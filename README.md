# BPC Studio

A portable toolkit for compelling written business plan competition proposals. Indonesian is the proposal default; English is supported. It combines commercial essay writing, customer and venture reasoning, driver-based finance, editable Word production, precise LaTeX/TikZ exhibits and a private source-and-lesson archive.

This packaged core prioritizes the working proposal workflow. Actual checks and the remaining source-visual gaps are stated in [validation](validation/README.md) and [release scope](RELEASE-NOTES.md).

Start at [START.md](START.md). Give an agent access to the repository, the current guidebook and your actual task. The agent follows [AGENTS.md](AGENTS.md) and [the operating entry](skills/build-bpc-proposals/SKILL.md). Loading the toolkit does not automatically generate a BMC, deck or pilot dossier.

## The writing standard

Present the complete intended business: why customers choose it, how value becomes revenue, how orders are fulfilled and why its economics can support repeat operation and growth. Describe adopted design directly while keeping real achievements and projections accurate. Detailed claim checks belong in working records; the proposal should read as connected, persuasive commercial reasoning.

## First commands

```bash
python -m pip install -r requirements.txt
python studio.py doctor
python studio.py new usaha-baru --language id
python studio.py --help
```

[Setup](docs/setup.md) covers virtual environments, Windows/macOS/Linux dependencies, fonts and tool commands. [Ruang Rapi](examples/ruang-rapi/README.md) is a synthetic worked example with inspectable inputs and representative output. [Validation](validation/README.md) distinguishes actual tests from remaining limits.

| Component | Entry |
|---|---|
| Single active operating manual | [BPC manual](skills/build-bpc-proposals/references/bpc-manual.md) |
| Writing system and bilingual repairs | [Commercial writing](skills/build-bpc-proposals/references/commercial-writing.md) |
| Adaptable page budgets and sections | [Proposal architecture](skills/build-bpc-proposals/references/proposal-architecture.md) |
| Markets, customer choices and evidence | [Venture reasoning](skills/build-bpc-proposals/references/venture-reasoning.md), [evidence](skills/build-bpc-proposals/references/evidence.md) |
| Finance and operating resources | [Finance](skills/build-bpc-proposals/references/finance.md), [operations](skills/build-bpc-proposals/references/operations.md) |
| LaTeX/TikZ exhibit preferences | [Visual system](skills/build-bpc-proposals/references/visual-system.md), [chart gallery](docs/chart-gallery.md), [reference images](docs/reference-atlas.md) |
| DOCX, rendering, comments and audit | [Production](skills/build-bpc-proposals/references/production.md), [document schema](docs/document-schema.md) |
| Optional BMC, pitch, script and Q&A | [Supporting formats](skills/build-bpc-proposals/references/supporting-formats.md) |
| Project continuity and handoff | [Continuity](skills/build-bpc-proposals/references/project-continuity.md) |
| Original references and per-document lessons | [Catalog](library/catalog.md), [reading routes](library/reading-routes.md), [BPC synthesis](library/bpc-synthesis.md), [58-document index](library/bpc-index.md) |

## Exact and editable exhibits

The existing chart engine supports issue trees, service flows, market layers, Gantt charts, risk heatmaps, comparisons, cash curves, distributions, sensitivity drivers, role structures, positioning and value propositions. Use reference images for information relationships and readable geometry. Recreate exhibits with the current project's data and assumptions. Keep input JSON, editable TeX, vector PDF and placement PNG together; preserve native Word tables for exact schedules. Compile and inspect actual placed output rather than assuming source code or a large image is readable.

## Repository use

Extract the ZIP, create an empty GitHub repository and upload this folder's contents. For the complete reference archive, Git is more practical than browser upload limits:

```bash
git init
git add .
git commit -m "Initialize BPC Studio"
git branch -M main
git remote add origin https://github.com/YOUR-ACCOUNT/BPC-Studio.git
git push -u origin main
```

The package contains no Git history, credentials, installed dependencies or personal skill installation. Local projects and output are ignored by default. Add a finished project deliberately if you want to version it.

Adapted from [Fafauzif/Essay-Studio](https://github.com/Fafauzif/Essay-Studio), commit `8fddfff968f492a1f13dc0bb7f97ca78bd09980a`. The older essay guidance and worked case are labeled historical. They cannot override the BPC entry or supply new-project facts. See [provenance notice](LICENSE-NOTICE.md) and [upstream inventory](archive/upstream-file-inventory.json). Third-party reference inclusion grants no blanket redistribution license.
