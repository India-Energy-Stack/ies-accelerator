#!/usr/bin/env bash
# Build a printed-book PDF of the IES Accelerator implementation guide.
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
COMBINED_MD="$BUILD_DIR/ies_combined.md"
OUT_PDF="$BUILD_DIR/ies_accelerator.pdf"

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

pandoc "$COMBINED_MD" \
    --output="$OUT_PDF" \
    --pdf-engine=tectonic \
    --from=markdown-task_lists \
    --toc \
    --toc-depth=2 \
    -V documentclass=report \
    -V geometry:margin=1in \
    -V monofont="Menlo" \
    --metadata title="IES Accelerator Implementation Guide" \
    --metadata author="India Energy Stack" \
    --metadata date="$(date +%Y-%m-%d)" \
    --resource-path="$REPO_ROOT" \
    2> "$BUILD_DIR/pandoc.log" || {
        echo "error: pandoc failed; see $BUILD_DIR/pandoc.log" >&2
        exit 1
    }

echo "Built: $OUT_PDF ($(du -h "$OUT_PDF" | cut -f1), $(grep -c '\\newpage' "$COMBINED_MD") chapters)"
