#!/usr/bin/env python3
"""Driver-based whole-order service model. No invented market data or financing."""
from pathlib import Path
import argparse, csv, hashlib, json, math

KEYS={'title','status','currency','price_year','price_basis','months','leads','conversion','repeat_rate','capacity','unit_price','unit_direct_cost','fixed_cost','marketing','equipment','setup_expense','depreciation_months','collection_lag','planned_funding','cash_floor','annual_discount_rate','metadata'}
FACTORS={'leads','price','direct_cost','fixed_cost'}

def numeric(x,name,lo=0,hi=None):
    if isinstance(x,bool) or not isinstance(x,(int,float)) or not math.isfinite(x) or x<lo or (hi is not None and x>hi):
        raise ValueError(f'{name} must be finite in [{lo}, {hi if hi is not None else "infinity"}]')
    return float(x)

def schedule(value,n,name,hi=None,whole=False):
    a=value if isinstance(value,list) else [value]*n
    if len(a)!=n:raise ValueError(f'{name} requires exactly {n} months')
    r=[numeric(x,name,hi=hi) for x in a]
    if whole and any(not x.is_integer() for x in r):raise ValueError(name+' must use whole quantities')
    return r

def model(c,factors=None):
    if not isinstance(c,dict):raise ValueError('Input must be an object')
    if set(c)-KEYS:raise ValueError('Unknown financial keys: '+', '.join(sorted(set(c)-KEYS)))
    n=c['months']
    if type(n) is not int or not 1<=n<=1200:raise ValueError('months must be 1..1200 integer')
    factors=factors or {}
    if set(factors)-FACTORS:raise ValueError('Unknown sensitivity factor')
    f={k:numeric(factors.get(k,1),k+' factor') for k in FACTORS}
    lead=schedule(c['leads'],n,'leads',whole=True);conv=schedule(c['conversion'],n,'conversion',hi=1)
    repeat=schedule(c.get('repeat_rate',0),n,'repeat_rate',hi=1);cap=schedule(c['capacity'],n,'capacity',whole=True)
    price=schedule(c['unit_price'],n,'unit_price');direct=schedule(c['unit_direct_cost'],n,'unit_direct_cost')
    fixed=schedule(c['fixed_cost'],n,'fixed_cost');marketing=schedule(c.get('marketing',0),n,'marketing')
    reserve=schedule(c.get('cash_floor',0),n,'cash_floor')
    equipment=numeric(c.get('equipment',0),'equipment');setup=numeric(c.get('setup_expense',0),'setup_expense');fund=numeric(c.get('planned_funding',0),'planned_funding');rate=numeric(c.get('annual_discount_rate',0),'annual_discount_rate')
    life=c.get('depreciation_months',36);lag=c.get('collection_lag',0)
    if type(life) is not int or life<1:raise ValueError('depreciation_months must be positive integer')
    if type(lag) is not int or not 0<=lag<=n:raise ValueError('collection_lag must be integer 0..months')
    cash=-equipment-setup;need=max(0,reserve[0]-cash);previous=0;rows=[];earned=[]
    for i in range(n):
        # Conservative whole-order floor; never fractional observed customers.
        available_leads=math.floor(lead[i]*f['leads']+1e-10)
        new=math.floor(available_leads*conv[i]+1e-10)
        returning=math.floor(previous*repeat[i]+1e-10)
        demand=new+returning;orders=min(demand,int(cap[i]));previous=orders
        revenue=orders*price[i]*f['price'];earned.append(revenue)
        costs=orders*direct[i]*f['direct_cost'];overhead=fixed[i]*f['fixed_cost'];spend=marketing[i]
        contribution=revenue-costs;ebitda=contribution-overhead-spend
        depreciation=equipment/life if i<life else 0;profit=ebitda-depreciation
        receipts=earned[i-lag] if i>=lag else 0
        net_cash=receipts-costs-overhead-spend;cash+=net_cash
        receivables=sum(earned)-sum(r['receipts'] for r in rows)-receipts
        need=max(need,reserve[i]-cash)
        unit_contribution=price[i]*f['price']-direct[i]*f['direct_cost']
        rows.append({'month':i+1,'qualified_leads':available_leads,'new_customer_demand':new,'repeat_order_demand':returning,'demand':demand,'capacity':int(cap[i]),'orders':orders,'unmet_orders':demand-orders,'unit_price':price[i]*f['price'],'unit_direct_cost':direct[i]*f['direct_cost'],'revenue':revenue,'direct_cost':costs,'contribution':contribution,'fixed_cost':overhead,'marketing':spend,'ebitda':ebitda,'depreciation':depreciation,'operating_profit':profit,'receipts':receipts,'net_operating_cash':net_cash,'receivables':receivables,'project_cash':cash,'funded_cash':cash+fund,'cash_floor':reserve[i],'reserve_headroom':cash+fund-reserve[i],'break_even_orders':math.ceil((overhead+spend)/unit_contribution-1e-10) if unit_contribution>0 else None,'marketing_per_new_customer_demand':spend/new if new else None})
    payback=next((r['month'] for j,r in enumerate(rows) if r['project_cash']>=0 and all(q['project_cash']>=0 for q in rows[j:])),None)
    additive=['orders','unmet_orders','revenue','direct_cost','contribution','fixed_cost','marketing','ebitda','depreciation','operating_profit','receipts','net_operating_cash']
    annual=[]
    for start in range(0,n,12):
        a=rows[start:start+12];annual.append({'year_index':start//12+1,'months':len(a),**{k:sum(r[k] for r in a) for k in additive},'closing_receivables':a[-1]['receivables'],'closing_project_cash':a[-1]['project_cash'],'closing_funded_cash':a[-1]['funded_cash']})
    return {'monthly':rows,'annual':annual,'summary':{**{k:sum(r[k] for r in rows) for k in additive},'initial_equipment':equipment,'initial_setup_expense':setup,'planned_funding':fund,'funding_need_including_floor':need,'funding_shortfall':max(0,need-fund),'closing_receivables':rows[-1]['receivables'],'closing_project_cash':cash,'closing_funded_cash':cash+fund,'minimum_reserve_headroom':min(fund-equipment-setup-reserve[0],*(r['reserve_headroom'] for r in rows)),'sustained_project_cash_payback_month':payback,'npv_before_financing':-equipment-setup+sum(r['net_operating_cash']/(1+rate)**(r['month']/12) for r in rows)}}

def calculate(c):
    base=model(c)
    cases=[]
    for key,change in [('price',.9),('price',1.1),('leads',.8),('leads',1.2),('direct_cost',1.1),('fixed_cost',1.1)]:
        s=model(c,{key:change})['summary'];cases.append({'factor':key,'multiplier':change,**s})
    return {'schema_version':1,'title':c.get('title'),'status':c.get('status','team planning assumptions'),'currency':c.get('currency','IDR'),'price_year':c.get('price_year'),'price_basis':c.get('price_basis'),'base':base,'sensitivity':cases,'scope':{'unit':'one fulfilled order per customer per month; integer floor for new and repeat demand; capacity capped; lost demand not carried forward','repeat':'previous month fulfilled orders multiplied by current repeat_rate; simple return-demand convention, not lifetime retention','cash':'all operating costs current-month; earned sales collected at integer lag; closing receivables not recovered automatically beyond horizon','profit':'operating profit before tax, interest and distributions; initial setup expense separate time-zero expense, not included again in monthly profit','funding':'planned time-zero equity cash only, no commitment implied; excluded from revenue/profit/project NPV','exclusions':['tax and VAT','debt and interest schedule','inventory and supplier credit','multi-product mix','terminal value','external market validation']}}

def write(c,out,input_path=None):
    out=Path(out);out.mkdir(parents=True,exist_ok=True);r=calculate(c)
    r['input_provenance']={'filename':Path(input_path).name if input_path else None,'sha256':hashlib.sha256(Path(input_path).read_bytes()).hexdigest() if input_path else None,'canonical_config_sha256':hashlib.sha256(json.dumps(c,sort_keys=True,ensure_ascii=False,allow_nan=False).encode('utf-8')).hexdigest()}
    raw=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+'\n';(out/'finance.json').write_text(raw,encoding='utf-8')
    rows=r['base']['monthly']
    with (out/'monthly.csv').open('w',newline='',encoding='utf-8') as fp:
        w=csv.DictWriter(fp,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
    charts=out/'chart-inputs';charts.mkdir(exist_ok=True)
    currency=c.get('currency','IDR');money_label='Rp' if currency=='IDR' else currency
    common={'font':'DejaVu Serif','font_pt':11,'width_cm':16,'example_status':c.get('status','team planning assumptions'),'source_note':f'Calculated from retained model input; {currency} divided by 1,000,000 for chart units.'}
    cash={**common,'id':'cash','type':'cash_line','periods':[0]+[x['month'] for x in rows],'x_label':'Bulan operasi','y_label':f'Kas (juta {money_label})','series':[{'label':'Kas proyek sebelum pendanaan','values':[-c.get('equipment',0)-c.get('setup_expense',0)]+[x['project_cash']/1e6 for x in rows]},{'label':'Kas setelah pendanaan','values':[(c.get('planned_funding',0)-c.get('equipment',0)-c.get('setup_expense',0))/1e6]+[x['funded_cash']/1e6 for x in rows]}]}
    cash['series'][0]['values'][0]/=1e6
    for name,value in [('cash',cash)]: (charts/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return r

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--out-dir',required=True,type=Path);a=p.parse_args()
    try:
        c=json.loads(a.input.read_text(encoding='utf-8'));r=write(c,a.out_dir,a.input)
        print(json.dumps({'output':str(a.out_dir),'summary':r['base']['summary'],'status':'calculated_not_market_validated'},ensure_ascii=False))
    except (KeyError,TypeError,ValueError,OSError) as e:p.exit(2,'Financial input error: '+str(e)+'\n')
if __name__=='__main__':main()
