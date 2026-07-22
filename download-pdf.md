# Download PDF

The entire GitBook — every chapter, every use-case guide, every schema overview — is also published as a single printable PDF.

**[⬇ Download ies-report.pdf](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf)**

---

## What's in it

Built from the same source as this GitBook, in the same order as the left-hand navigation: Getting Started, Glossary, FAQ, What IES Provides (Register → Discover → Exchange → Electricity Credentials), How you implement IES, Use Case Overviews, Use Case Implementation Guides, and Reference — followed by an **Appendix — Schemas Reference** at the end, covering Schemas Overview and the field reference for every schema family.

The appendix is placed last and behind a clear divider chapter on purpose: the document is long, and the schema field-reference tables are lookup material, not narrative reading. Putting them at the end keeps the front of the PDF a clean, linear read, while still shipping the complete schema reference inside the same file.

## How it's kept current

Rebuilt automatically by a GitHub Actions workflow ([`build-pdf.yml`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/workflows/build-pdf.yml)) on every merge to `main`. There's no separate "publish" step — whatever is live on this GitBook is what the PDF reflects, usually within a couple of minutes.

## Building it yourself

The same PDF can be built locally from a clone of the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator):

```bash
brew install pandoc tectonic          # macOS; see the workflow file for Linux packages
npx -y @mermaid-js/mermaid-cli --version   # confirms mmdc is available for diagrams
bash scripts/build_pdf.sh
```

This produces `build/ies_accelerator.pdf` — the exact file the GitHub Actions workflow publishes.
