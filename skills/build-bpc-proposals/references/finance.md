# Finance from business drivers

Define currency, price year/basis, period, payer, deliverable, earned unit, collection timing and operating capacity before calculating. Separate customers, orders, units, GMV, company revenue, contribution, profit, project cash and financing. Reference proposal numbers are never default business assumptions.

Use `python studio.py finance INPUT.json --out-dir OUTPUT`. See [the complete input](../../../examples/ruang-rapi/finance-input.json). This driver model writes finance.json, native-table-ready monthly.csv and calculated cash-chart input. `analyze finance` retains the simpler inherited model documented in [calculation tools](../../../docs/calculation-tools.md). Choose or extend the model to fit the business rather than forcing every venture into one schema.

## Model conventions

Qualified leads × conversion generates new-customer demand. The repeat rate applies to the previous month's fulfilled orders under an explicit one-order-per-customer-per-month convention. Both quantities are floored to whole orders. Demand is capped by scheduled capacity; unmet demand is shown and not carried forward. This is a simple return-demand model, not lifetime retention. Marketing spending is explicit; spending divided by new demand is not an independently measured CAC, especially when capacity limits fulfillment.

Revenue equals fulfilled orders × unit price. Direct cost equals orders × direct unit cost. Contribution is revenue minus direct cost. EBITDA deducts fixed costs and marketing; operating profit also deducts straight-line equipment depreciation. Setup expense is an initial expense/payment outside the monthly operating-profit series. State it separately when interpreting total project-period profit.

Equipment and setup are paid at time zero. Operating costs are paid currently. Earned sales are collected after the stated integer-month lag. Closing receivables are cumulative revenue less receipts and are not automatically recovered beyond the horizon. Planned funding enters cash at time zero; it is not revenue, profit or project NPV. A reserve floor is a required balance, not an expense.

Funding need is the greatest shortfall from the floor, including time zero. Sustained project cash payback is the first nonnegative project-cash month after which it remains nonnegative through the horizon. It differs from recurring break-even orders, first positive EBITDA and positive funded cash. NPV discounts pre-financing cash using an annual effective rate raised to month/12, with no invented terminal value.

The model excludes taxes/VAT, debt/interest, inventory, supplier credit, multi-product cohorts and owner distributions. Outputs are operating results before tax and financing costs. Add material features in a project-specific extension; do not call the generic output after-tax net profit.

## Meaningful input discipline

Use explicit monthly schedules for lead ramp, capacity, price, direct cost, fixed resources and marketing when they change. Unknown keys, nonfinite values, negative quantities, inconsistent arrays and invalid rates are rejected. Retain component costs and staffing/capacity rationale in metadata. Treat founder labor as a paid resource or disclose its noncash economic cost. Planned capital is not committed funding.

For a constant configuration, recurring break-even orders equal fixed and marketing costs divided by unit contribution, rounded up. If marketing is marginal per order, put that marginal amount in contribution instead. Margin on sales divides contribution by price; markup divides it by cost. Define the included costs and period before interpreting either.

## Sensitivity and writing

One-factor sensitivity recalculates price ±10%, qualified leads ±20%, direct costs +10% and fixed costs +10% through the same demand/capacity/cash engine. These are conditional planning cases, not probabilities. Choose additional adverse ranges based on the actual business. Use optional Monte Carlo only when joint uncertainty changes a decision; document marginals, dependence, seed, draw order and stability.

Explain what contribution pays for, where cash is tight and what growth requires. Keep material assumptions beside the financial consequence, without apologizing for every forecast. A positive operating profit with negative pre-financing cash can be coherent when receivables and investment explain the bridge.

## Reconciliation

Independently reconstruct representative monthly orders, capacity, price × quantity, direct costs, all annual sums, receivables, cash bridge, reserve need, break-even and decisive downside. Compare unrounded values across JSON/CSV, Word tables, narrative and chart inputs. See [sample reconciliation](../../../examples/ruang-rapi/reconcile.py). Rounding is presentation only. Rendering proves layout; arithmetic proves a conditional model; neither proves demand.
