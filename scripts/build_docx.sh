#!/usr/bin/env bash
# Build the Word (.docx) deliverable from the curated manifest SUMMARY.docx.md
# (the technical reference WITHOUT Propose a Schema, Pathways and draft/).
#
# Requirements:
#   - pandoc  (brew install pandoc)
#   - mmdc    (npm i -g @mermaid-js/mermaid-cli) -- optional; without it,
#             mermaid diagrams render as code blocks.
#
# Rerun this any time the docs change:  bash scripts/build_docx.sh
#
# Output: build/IES_Technical_Reference.docx

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
python3 "$REPO_ROOT/scripts/build_docx.py" "$@"
