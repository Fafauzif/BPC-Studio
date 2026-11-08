# Ruang Rapi worked example

A complete compact synthetic written business proposal, not actual sales, research, partnership or funding. Its source input and calculations deliberately distinguish operating profit from cash and preserve a negative first-year project cash/NPV result.

```bash
python studio.py finance examples/ruang-rapi/finance-input.json --out-dir examples/ruang-rapi/model
python studio.py chart examples/ruang-rapi/model/chart-inputs/cash.json --out-dir examples/ruang-rapi/assets/charts
python examples/ruang-rapi/build_sample.py
python studio.py build examples/ruang-rapi/proposal.json --output examples/ruang-rapi/proposal.docx
python studio.py render examples/ruang-rapi/proposal.docx --out-dir examples/ruang-rapi/render
python examples/ruang-rapi/reconcile.py
```

Editable inputs: finance-input.json and proposal.json. Model: model/finance.json and monthly.csv. Chart: input JSON, editable TeX, vector PDF and PNG. Native Word schedules and clickable appendix/return navigation are in proposal.docx. The rendered export is render/proposal.pdf.

The example uses DejaVu Serif11pt,1.15spacing,A4,2.5cm margins and a three-body-page budget chosen for demonstration; these are not universal competition rules. The twelve-month model includes current-month operating payments, one-month collections lag, equipment depreciation and time-zero equity. It excludes tax, debt, inventory and terminal recovery. Replicate the business’s actual assumptions for real work.
