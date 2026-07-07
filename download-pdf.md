# Download PDF

The entire GitBook — every chapter, every use-case guide, every schema overview — is also published as a single printable PDF.

**[⬇ Download ies-report.pdf](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf)**

---

## What's in it

The PDF is built from the same source as this GitBook, in the same order as the left-hand navigation: Home, Getting Started, Glossary, What IES Provides (Register → Discover → Exchange, Schemas Overview, Taxonomy), How you implement IES, Use Case Implementation Guides, and Reference.

## How it's kept current

The PDF is rebuilt automatically by a GitHub Actions workflow ([`build-pdf.yml`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/workflows/build-pdf.yml)) every time a change merges to the `main` branch. There is no separate "publish" step — whatever is live on this GitBook is what the PDF reflects, usually within a couple of minutes of a merge.

## Building it yourself

The same PDF can be built locally from a clone of the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator):

```bash
brew install pandoc tectonic          # macOS; see the workflow file for Linux packages
npx -y @mermaid-js/mermaid-cli --version   # confirms mmdc is available for diagrams
bash scripts/build_pdf.sh
```

This produces `build/ies_accelerator.pdf` — the exact file the GitHub Actions workflow publishes.
