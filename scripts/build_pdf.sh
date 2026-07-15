#!/usr/bin/env bash
# Build a single printed-book PDF of the IES Accelerator implementation guide.
# All schema content (Schemas Overview + Taxonomy field reference) is moved
# to a clearly divided "Appendix — Schemas Reference" chapter at the end,
# instead of interleaved with the narrative in SUMMARY.md order — see
# scripts/build_pdf.py.
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
# Output: build/ies_accelerator.pdf

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

COMBINED_MD="$BUILD_DIR/ies_combined.md"
OUT_PDF="$BUILD_DIR/ies_accelerator.pdf"

# Tighter margins and a smaller base font than the LaTeX report-class
# defaults, cutting page count with no content change — still comfortably
# readable for a printed technical guide.
pandoc "$COMBINED_MD" \
    --output="$OUT_PDF" \
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
    --metadata title="IES Accelerator Implementation Guide" \
    --metadata author="India Energy Stack" \
    --metadata date="$(date +%Y-%m-%d)" \
    --resource-path="$REPO_ROOT" \
    2> "$BUILD_DIR/pandoc.log" || {
        echo "error: pandoc failed; see $BUILD_DIR/pandoc.log" >&2
        exit 1
    }

echo "Built: $OUT_PDF ($(du -h "$OUT_PDF" | cut -f1))"
