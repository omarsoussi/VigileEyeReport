# VigileEyeReport — Setup & Build

Quick instructions for a collaborator to get the project locally, add the remote, and build the PDF report.

**Prerequisites**
- Git installed (`git --version`).
- TeX toolchain with XeLaTeX and `latexmk`:
  - macOS: install MacTeX or BasicTeX (e.g. `brew install --cask mactex`).
  - Debian/Ubuntu: `sudo apt update && sudo apt install -y texlive-xetex texlive-latex-extra latexmk`.
  - Windows: install MiKTeX or TeX Live and ensure `latexmk` is available.

**Clone the repo (recommended)**

```bash
# clone the origin repository
git clone https://github.com/omarsoussi/VigileEyeReport.git
cd VigileEyeReport
```

If you already have the project locally and want to add the upstream origin remote and push the `main` branch, run:

```bash
git remote add origin https://github.com/omarsoussi/VigileEyeReport.git
git branch -M main
git push -u origin main
```

**Build the report (PDF)**

This project includes a `.latexmkrc` configured to use XeLaTeX. From the project root run:

```bash
# clean old build files (optional)
latexmk -C
# build PDF (latexmk will use the .latexmkrc settings)
latexmk -pdf
# the output will be `main.pdf` in the project root
```

On macOS you can open the result with `open main.pdf`. On Linux use your PDF viewer (e.g. `xdg-open main.pdf`).

**Notes & troubleshooting**
- If fonts are missing, install a standard font package (MacTeX includes many fonts). The TeX source falls back to `Times New Roman` if `TeX Gyre Termes` isn't present.
- If `latexmk` is not found, install it via your TeX distribution or package manager.
- If images or diagrams are missing, ensure any external diagram files exist under the repository paths shown in the project tree.

If you want, I can also create a small script (`build.sh`) to automate the build steps and clean/push hooks — tell me and I will add it.

---
Created for quick onboarding — feel free to edit or ask for extra platform-specific steps.
