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
#
# No --number-sections: the source headings already carry their own manual
# numbers (e.g. "2.4 — Confirm your DeDi namespace is live", "11. Points for
# Confirmation") which the GitBook web view and the in-text §-cross-references
# rely on. Letting LaTeX auto-number on top of those produced double numbering
# in the TOC ("14.5  2.4 Confirm your DeDi namespace is live"). Without the
# flag, pandoc sets secnumdepth to -\maxdimen (no auto numbering) and the TOC
# shows only the authored numbers — matching the web exactly.
#
# --lua-filter=pdf_breakable_code.lua gives long inline code spans explicit
# breakpoints. Without it a path like
# `credentialSubject.customerProfile.consumptionProfiles[].meterId` is one
# unbreakable box that overruns its 0.2\linewidth table column and prints on
# top of the next column — see the filter's header for the full story.
#
# The \texttt redefinition switches hyphenation off for monospaced text
# (\hyphenchar = -1 for the current tt font). TeX would otherwise break
# `.attributes.serialNumber` as ".at-" / "tributes.serialNumber", and an
# invented hyphen inside a JSON path reads as part of the path. With the
# filter supplying real breakpoints, nothing needs hyphenation to fit.
#
# fvextra wraps long lines inside code blocks. Neither LaTeX's verbatim nor
# pandoc's Highlighting environment breaks lines, so a 100-character JSON-LD
# @context URL in an example ran past the right margin and off the edge of
# the paper — the tail of the line was not just ugly, it was gone. Both
# environments are redefined here because the examples use a mix of tagged
# (```json, ```bash) and untagged fences.
#
# The wider \emergencystretch (pandoc's template sets 3em) lets TeX loosen a
# line rather than let it stick out. Breakpoints alone are not always enough:
# with a long code span such as `ELECTRICITY/GAS/WATER/HEAT` near the end of a
# justified line, taking the break needs more stretch than 3em can supply, so
# TeX kept the overfull line instead.
pandoc "$COMBINED_MD" \
    --output="$OUT_PDF" \
    --pdf-engine=tectonic \
    --from=markdown-task_lists \
    --lua-filter="$REPO_ROOT/scripts/pdf_breakable_code.lua" \
    --toc \
    --toc-depth=2 \
    -V documentclass=report \
    -V geometry:margin=0.75in \
    -V fontsize=10pt \
    -V monofont="${MONOFONT:-Menlo}" \
    -V graphics=true \
    -V header-includes='\usepackage{graphicx}' \
    -V header-includes='\let\IESorigtexttt\texttt\renewcommand{\texttt}[1]{\IESorigtexttt{\hyphenchar\font=-1\relax #1}}' \
    -V header-includes='\usepackage{fvextra}\DefineVerbatimEnvironment{Highlighting}{Verbatim}{commandchars=\\\{\},breaklines,breakanywhere,breakafter=/}\RecustomVerbatimEnvironment{verbatim}{Verbatim}{breaklines,breakanywhere,breakafter=/}' \
    -V header-includes='\setlength{\emergencystretch}{6em}' \
    --metadata title="IES Accelerator Implementation Guide" \
    --metadata author="India Energy Stack" \
    --metadata date="$(git -C "$REPO_ROOT" show -s --format=%cs HEAD)" \
    --resource-path="$REPO_ROOT" \
    2> "$BUILD_DIR/pandoc.log" || {
        echo "error: pandoc failed; see $BUILD_DIR/pandoc.log" >&2
        exit 1
    }

echo "Built: $OUT_PDF ($(du -h "$OUT_PDF" | cut -f1))"
