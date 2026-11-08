#!/usr/bin/env python3
"""Independently reconcile this synthetic teaching sample; never import finance.py.

Uses Decimal money arithmetic and a hand-reviewed whole-order schedule. Run after
regenerating model outputs. A pass establishes calculation consistency only.
"""
from pathlib import Path
from decimal import Decimal as D, ROUND_FLOOR
import argparse,csv,hashlib,json,math

BASE=Path(__file__).resolve().parent
EXPECTED_ORDERS=[20,26,29,31,34,36,39,40,44,46,48,48]
def dec(x):return D(str(x))
def at(c,key,i,default=0):
 value=c.get(key,default);return dec(value[i] if isinstance(value,list) else value)
def reconcile(base=BASE):
 base=Path(base);source=base/'finance-input.json';result=base/'model/finance.json';csvfile=base/'model/monthly.csv'
 c=json.loads(source.read_text(encoding='utf-8'));r=json.loads(result.read_text(encoding='utf-8'));rows=r['base']['monthly']
 with csvfile.open(encoding='utf-8',newline='') as fp:csvrows=list(csv.DictReader(fp))
 failures=[];checks=0
 def check(name,actual,expected,tolerance=D('.01')):
  nonlocal checks
  checks+=1
  same=actual==expected if expected is None else abs(dec(actual)-dec(expected))<=tolerance
  if not same:failures.append({'check':name,'actual':actual,'expected':str(expected) if isinstance(expected,D) else expected})
 check('sample horizon',len(rows),12);check('CSV row count',len(csvrows),12)
 check('unit direct cost breakdown',sum(map(dec,c['metadata']['direct_cost_breakdown'].values())),c['unit_direct_cost'])
 check('fixed monthly cost breakdown',sum(map(dec,c['metadata']['fixed_cost_breakdown'].values())),c['fixed_cost'])
 equipment=dec(c['equipment']);setup=dec(c['setup_expense']);fund=dec(c['planned_funding']);cash=-equipment-setup;need=max(D(0),at(c,'cash_floor',0)-cash)
 cashflows=[];revenues=[];expected_rows=[]
 for i,orders in enumerate(EXPECTED_ORDERS):
  new=int((at(c,'leads',i)*at(c,'conversion',i)).to_integral_value(rounding=ROUND_FLOOR))
  repeat=int((dec(EXPECTED_ORDERS[i-1] if i else 0)*at(c,'repeat_rate',i)).to_integral_value(rounding=ROUND_FLOOR))
  check(f'month {i+1} hand-reviewed orders',min(new+repeat,int(at(c,'capacity',i))),orders)
  revenue=dec(orders)*at(c,'unit_price',i);direct=dec(orders)*at(c,'unit_direct_cost',i)
  overhead=at(c,'fixed_cost',i);marketing=at(c,'marketing',i);contribution=revenue-direct;ebitda=contribution-overhead-marketing
  depreciation=equipment/dec(c['depreciation_months']) if i<c['depreciation_months'] else D(0)
  revenues.append(revenue);lag=c['collection_lag'];receipts=revenues[i-lag] if i>=lag else D(0)
  flow=receipts-direct-overhead-marketing;cash+=flow;cashflows.append(flow);need=max(need,at(c,'cash_floor',i)-cash)
  receivables=sum(revenues)-sum(x['receipts'] for x in expected_rows)-receipts
  values={'orders':orders,'new_customer_demand':new,'repeat_order_demand':repeat,'unmet_orders':new+repeat-orders,
   'revenue':revenue,'direct_cost':direct,'contribution':contribution,'fixed_cost':overhead,'marketing':marketing,
   'ebitda':ebitda,'depreciation':depreciation,'operating_profit':ebitda-depreciation,'receipts':receipts,
   'net_operating_cash':flow,'project_cash':cash,'funded_cash':cash+fund,'receivables':receivables,
   'reserve_headroom':cash+fund-at(c,'cash_floor',i),'break_even_orders':25}
  expected_rows.append(values)
  if i<len(rows):
   for key,value in values.items():check(f'month {i+1} {key}',rows[i][key],value)
  if i<len(csvrows):
   for key,value in values.items():check(f'CSV month {i+1} {key}',csvrows[i][key],value)
 s=r['base']['summary']
 for key in ['orders','unmet_orders','revenue','direct_cost','contribution','fixed_cost','marketing','ebitda','depreciation','operating_profit','receipts','net_operating_cash']:
  total=sum(dec(x[key]) for x in expected_rows);check('summary '+key,s[key],total)
  check('annual '+key,r['base']['annual'][0][key],total)
 for key,expected in {'funding_need_including_floor':need,'funding_shortfall':max(0,need-fund),'closing_project_cash':cash,'closing_funded_cash':cash+fund,'closing_receivables':expected_rows[-1]['receivables'],'sustained_project_cash_payback_month':None}.items():check('summary '+key,s[key],expected)
 npv=float(-equipment-setup)+sum(float(flow)/(1+float(c['annual_discount_rate']))**((i+1)/12) for i,flow in enumerate(cashflows))
 check('independent discounted cash NPV',s['npv_before_financing'],npv)
 check('cash excludes closing receivable recovery',cash,-1400000)
 check('planned funding excludes company revenue',s['revenue'],198450000)
 return {'status':'pass' if not failures else 'fail','checks':checks,'failures':failures,
  'inputs_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'model_sha256':hashlib.sha256(result.read_bytes()).hexdigest(),'csv_sha256':hashlib.sha256(csvfile.read_bytes()).hexdigest(),
  'method':'Independent Decimal schedules and hand-reviewed order vector; finance.py is not imported.',
  'scope':'Synthetic teaching inputs only; checks arithmetic, timing, capacity and funding separation. No customer-demand, market, tax or operational validation.'}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path);a=p.parse_args();r=reconcile();raw=json.dumps(r,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
 if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(raw,encoding='utf-8')
 print(raw);return 0 if r['status']=='pass' else 1
if __name__=='__main__':raise SystemExit(main())
