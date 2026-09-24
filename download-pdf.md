# Download PDF

The deliverable subset of this GitBook — the narrative chapters and the full schemas reference — is published as a single printable PDF.

**[⬇ Download ies-report.pdf](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf)**

---

## What's in it

The PDF is built from a curated print manifest ([`SUMMARY.print.md`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/SUMMARY.print.md)), not from the full left-hand navigation: Home, Glossary, FAQ, What IES Provides (Register → Discover → Exchange → Verifiable Credentials → Security → Schemas Overview), the finalised Use Case Overviews — followed by an **Appendix — Schemas Reference** at the end, covering the field reference for every schema family.

The appendix is placed last and behind a clear divider chapter on purpose: the schema field-reference tables are lookup material, not narrative reading. Putting them at the end keeps the front of the PDF a clean, linear read, while still shipping the complete schema reference inside the same file.

Developer material — How you implement IES, the Use Case Implementation Guides, and the developer schema catalog — plus site-only pages (Status, Pathways, Propose a Schema, Contributors, this page) and anything marked WIP or Draft stay in this GitBook and are deliberately not part of the printed PDF.

## How it's kept current

Pull requests build and verify a staged PDF and public-site preview through [`build-pdf.yml`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/workflows/build-pdf.yml). After an accepted change lands on `main`, the separate main-only [`publish-pages.yml`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/workflows/publish-pages.yml) workflow rebuilds the same source, repeats the publication checks, and deploys the verified PDF and public files to GitHub Pages. GitBook and the PDF are sourced from the repository, but each hosted surface still requires its own post-publication verification.

## Building it yourself

The same PDF can be built locally from a clone of the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator):

```bash
brew install pandoc tectonic          # macOS; see the workflow file for Linux packages
npx -y @mermaid-js/mermaid-cli --version   # confirms mmdc is available for diagrams
bash scripts/build_pdf.sh
```

This produces `build/ies_accelerator.pdf` — the document the GitHub Actions preview validates and the main-only publication workflow deploys as [`ies-report.pdf`](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf).
