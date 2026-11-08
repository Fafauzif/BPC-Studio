"""Independent hand-calculated cash, order and accounting cases for the service model."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('service_finance',ROOT/'skills/build-bpc-proposals/scripts/finance.py')
finance=importlib.util.module_from_spec(spec);spec.loader.exec_module(finance)

def fixture():
 return {'months':3,'leads':10,'conversion':.5,'repeat_rate':.5,'capacity':[3,10,10],
         'unit_price':100,'unit_direct_cost':40,'fixed_cost':50,'marketing':10,
         'equipment':120,'setup_expense':30,'depreciation_months':3,'collection_lag':1,
         'planned_funding':400,'cash_floor':20,'annual_discount_rate':0}

class ServiceFinance(unittest.TestCase):
 def test_hand_calculated_three_month_case(self):
  r=finance.model(fixture());rows=r['monthly'];s=r['summary']
  self.assertEqual([x['orders'] for x in rows],[3,6,8])
  self.assertEqual([x['repeat_order_demand'] for x in rows],[0,1,3])
  self.assertEqual([x['unmet_orders'] for x in rows],[2,0,0])
  self.assertEqual([x['receipts'] for x in rows],[0,300,600])
  self.assertEqual([x['project_cash'] for x in rows],[-330,-330,-110])
  expected={'orders':17,'revenue':1700,'direct_cost':680,'ebitda':840,'depreciation':120,
            'operating_profit':720,'receipts':900,'closing_receivables':800,
            'closing_project_cash':-110,'closing_funded_cash':290,'funding_need_including_floor':350,
            'funding_shortfall':0,'minimum_reserve_headroom':50,'npv_before_financing':-110,
            'sustained_project_cash_payback_month':None}
  for key,value in expected.items():self.assertEqual(s[key],value,key)
 def test_financing_changes_only_financing_results(self):
  c=fixture();funded=finance.model(c);c['planned_funding']=0;unfunded=finance.model(c)
  for key in ['revenue','ebitda','operating_profit','npv_before_financing','closing_project_cash','funding_need_including_floor']:
   self.assertEqual(funded['summary'][key],unfunded['summary'][key],key)
  for a,b in zip(funded['monthly'],unfunded['monthly']):self.assertEqual(a['funded_cash']-b['funded_cash'],400)
 def test_receivables_are_not_automatically_recovered_at_horizon(self):
  c=fixture();c['collection_lag']=3;r=finance.model(c)
  self.assertEqual(r['summary']['receipts'],0);self.assertEqual(r['summary']['closing_receivables'],1700)
  self.assertEqual(r['summary']['npv_before_financing'],-1010)
 def test_fractional_and_nonfinite_operating_inputs_rejected(self):
  for key,value in [('leads',1.5),('capacity',2.5),('conversion',1.01),('repeat_rate',-1),('unit_price',float('inf')),('collection_lag',True),('months',0)]:
   with self.subTest(key=key):
    c=fixture();c[key]=value
    with self.assertRaises(ValueError):finance.model(c)
  c=fixture();c['tax']=.1
  with self.assertRaisesRegex(ValueError,'Unknown'):finance.model(c)
 def test_whole_order_floor_and_zero_contribution(self):
  c=fixture();c.update(leads=3,conversion=.5,repeat_rate=.75,capacity=10,unit_price=40)
  r=finance.model(c);self.assertEqual([x['orders'] for x in r['monthly']],[1,1,1])
  self.assertTrue(all(x['break_even_orders'] is None for x in r['monthly']))
 def test_depreciation_stops_after_asset_life(self):
  c=fixture();c['depreciation_months']=2;r=finance.model(c)
  self.assertEqual([x['depreciation'] for x in r['monthly']],[60,60,0])
  self.assertEqual(r['summary']['operating_profit'],720)
 def test_annual_aggregation_and_monthly_discount_convention(self):
  c=fixture();c.update(months=13,capacity=10,leads=0,equipment=120,setup_expense=0,fixed_cost=0,marketing=0,collection_lag=0,depreciation_months=12)
  r=finance.model(c);self.assertEqual([a['months'] for a in r['annual']],[12,1])
  self.assertEqual([a['depreciation'] for a in r['annual']],[120,0])
  c={'months':1,'leads':1,'conversion':1,'capacity':1,'unit_price':120,'unit_direct_cost':0,'fixed_cost':0,'annual_discount_rate':.12}
  self.assertAlmostEqual(finance.model(c)['summary']['npv_before_financing'],120/(1.12**(1/12)))
 def test_cash_chart_initial_values_have_same_scale_as_months(self):
  with tempfile.TemporaryDirectory() as d:
   finance.write(fixture(),d);chart=json.loads((Path(d)/'chart-inputs/cash.json').read_text())
   self.assertEqual(chart['series'][0]['values'],[-.00015,-.00033,-.00033,-.00011])
   self.assertEqual(chart['series'][1]['values'],[.00025,.00007,.00007,.00029])

if __name__=='__main__':unittest.main()
