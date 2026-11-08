# Setup and working commands

Use Python 3.10 or newer. Create a virtual environment and install dependencies:

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python studio.py doctor
python studio.py new usaha-baru --language id
```

DOCX creation needs python-docx, Pillow and lxml. PDF intake/render inspection needs PyMuPDF. Optional OCR needs Tesseract and its language packs. PDF conversion needs LibreOffice; put it on PATH or set LIBREOFFICE_BIN to the full executable path. Precise charts need XeLaTeX or LuaLaTeX, TikZ/PGFPlots/standalone/fontspec and an installed requested font. DejaVu Serif is used by the portable demonstration; install that family or explicitly choose another available family and inspect the output. Guidebook-required fonts must be genuinely installed.

On Debian/Ubuntu a typical optional system installation is `sudo apt install libreoffice-writer poppler-utils tesseract-ocr tesseract-ocr-ind texlive-xetex texlive-pictures texlive-latex-extra fonts-dejavu`. On Windows use the official Python, LibreOffice, Tesseract and MiKTeX/TeX Live installers and add their executables to PATH. The toolkit does not install them automatically.

```bash
python studio.py read inputs/guidebook.pdf --out-dir projects/usaha-baru/evidence/intake
python studio.py build examples/ruang-rapi/proposal.json --output output/proposal.docx
python studio.py render output/proposal.docx --out-dir output/render
python studio.py audit output/proposal.docx --pdf output/render/proposal.pdf --project examples/ruang-rapi/proposal.json --output output/audit.json
python studio.py chart --help
python studio.py finance --help
python studio.py voice projects/usaha-baru/draft.md
python studio.py handoff usaha-baru
python studio.py verify-library
python studio.py check
python -m unittest discover -s tests -v
```

Read each subcommand's help for its exact interface. `doctor` reports availability, not functional success. The `validation/` records describe the supplied release; your actual environment and future inputs need their own checks. No API key, installed personal skill, temporary URL or private account is needed for local tools.
