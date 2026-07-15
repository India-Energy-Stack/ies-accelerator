#!/usr/bin/env bash
# Build two printed-book PDFs from the GitBook:
#   - ies_accelerator.pdf         narrative + implementation guide (published as ies-report.pdf)
#   - ies_accelerator_schemas.pdf schemas overview + taxonomy field reference
#                                 (published as IES_proposed_schemas.pdf)
#
# Requirements:
#   - pandoc       (brew install pandoc)
#   - tectonic     (brew install tectonic)
#   - mmdc         (npx -y @mermaid-js/mermaid-cli) -- optional; if absent,
#                  mermaid blocks render as code instead of diagrams.
#
# Optional env vars:
#   PUPPETEER_EXECUTABLE_PATH  Path to a Chrome/Chromium binary. If set, the
#                              script writes a puppeteer config so mermaid-cli
#                              uses it instead of downloading Chromium.
#
# Output: build/ies_accelerator.pdf, build/ies_accelerator_schemas.pdf

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BUILD_DIR="$REPO_ROOT/build"
MERMAID_DIR="$BUILD_DIR/mermaid"

mkdir -p "$MERMAID_DIR"

require() {
    command -v "$1" >/dev/null 2>&1 || { echo "error: '$1' not found on PATH. $2" >&2; exit 1; }
}

require pandoc   "Install with: brew install pandoc"
require tectonic "Install with: brew install tectonic"

if ! command -v mmdc >/dev/null 2>&1; then
    echo "note: mmdc not found; mermaid diagrams will render as code blocks."
    echo "      To enable diagram rendering: npm i -g @mermaid-js/mermaid-cli"
fi

if [[ -n "${PUPPETEER_EXECUTABLE_PATH:-}" ]]; then
    cat > "$MERMAID_DIR/puppeteer.json" <<EOF
{"executablePath": "$PUPPETEER_EXECUTABLE_PATH", "args": ["--no-sandbox"]}
EOF
fi

python3 "$REPO_ROOT/scripts/build_pdf.py"

# Shared pandoc settings: tighter margins and a smaller base font than the
# LaTeX report-class defaults, cutting page count with no content change —
# still comfortably readable for a printed technical guide.
build_pdf() {
    local combined_md="$1" out_pdf="$2" title="$3"
    pandoc "$combined_md" \
        --output="$out_pdf" \
        --pdf-engine=tectonic \
        --from=markdown-task_lists \
        --toc \
        --toc-depth=2 \
        --number-sections \
        -V secnumdepth=2 \
        -V documentclass=report \
        -V geometry:margin=0.75in \
        -V fontsize=10pt \
        -V monofont="${MONOFONT:-Menlo}" \
        -V graphics=true \
        -V header-includes='\usepackage{graphicx}' \
        --metadata title="$title" \
        --metadata author="India Energy Stack" \
        --metadata date="$(date +%Y-%m-%d)" \
        --resource-path="$REPO_ROOT" \
        2> "$BUILD_DIR/$(basename "$out_pdf" .pdf).log" || {
            echo "error: pandoc failed on $combined_md; see $BUILD_DIR/$(basename "$out_pdf" .pdf).log" >&2
            exit 1
        }
    echo "Built: $out_pdf ($(du -h "$out_pdf" | cut -f1))"
}

build_pdf "$BUILD_DIR/ies_combined.md" "$BUILD_DIR/ies_accelerator.pdf" "IES Accelerator Implementation Guide"
build_pdf "$BUILD_DIR/ies_schemas_combined.md" "$BUILD_DIR/ies_accelerator_schemas.pdf" "IES Proposed Schemas"
