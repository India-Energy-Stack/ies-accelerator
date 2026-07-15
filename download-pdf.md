# Download PDF

The GitBook is also published as two printable PDFs.

**[⬇ Download ies-report.pdf](https://india-energy-stack.github.io/ies-accelerator/ies-report.pdf)** — the narrative and implementation guide.

**[⬇ Download IES_proposed_schemas.pdf](https://india-energy-stack.github.io/ies-accelerator/IES_proposed_schemas.pdf)** — the Schemas Overview and Taxonomy field reference.

---

## What's in each

| PDF | Covers |
|---|---|
| `ies-report.pdf` | Home, Getting Started, Glossary, What IES Provides (Register → Discover → Exchange), How you implement IES, Use Case Overviews, Use Case Implementation Guides, and Reference |
| `IES_proposed_schemas.pdf` | Schemas Overview (plain-language walkthroughs) and Taxonomy (the auto-generated field-reference tables for every schema family) |

Both are built from the same source as this GitBook, in the same order as the left-hand navigation.

## How they're kept current

Rebuilt automatically by a GitHub Actions workflow ([`build-pdf.yml`](https://github.com/India-Energy-Stack/ies-accelerator/blob/main/.github/workflows/build-pdf.yml)) on every merge to `main`. There's no separate "publish" step — whatever is live on this GitBook is what the PDFs reflect, usually within a couple of minutes.

## Building them yourself

Both PDFs build locally from a clone of the [ies-accelerator repository](https://github.com/India-Energy-Stack/ies-accelerator):

```bash
brew install pandoc tectonic          # macOS; see the workflow file for Linux packages
npx -y @mermaid-js/mermaid-cli --version   # confirms mmdc is available for diagrams
bash scripts/build_pdf.sh
```

This produces `build/ies_accelerator.pdf` and `build/ies_accelerator_schemas.pdf` — the exact files the GitHub Actions workflow publishes as `ies-report.pdf` and `IES_proposed_schemas.pdf`.
