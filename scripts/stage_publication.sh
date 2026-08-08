#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

mkdir -p public
# Mirror the repository content served by GitHub Pages while excluding
# engineering-only QAQC evidence and the retired generated Markdown index.
rsync -a \
  --exclude='.git/' \
  --exclude='.github/' \
  --exclude='build/' \
  --exclude='public/' \
  --exclude='qaqc/' \
  --exclude='index.md' \
  ./ public/

cp build/ies_accelerator.pdf public/ies-report.pdf
touch public/.nojekyll
cat > public/index.html <<'HTML'
<!doctype html>
<meta charset="utf-8">
<title>India Energy Stack (IES) — Technical Documentation</title>
<meta http-equiv="refresh" content="0; url=ies-report.pdf">
<p><a href="ies-report.pdf">India Energy Stack (IES) — Technical Documentation (PDF)</a></p>
HTML

missing=0
while IFS= read -r file; do
  if [ ! -f "public/$file" ]; then
    echo "MISSING: $file"
    missing=1
  fi
done < <(git ls-files schemas/)
[ -f public/ies-report.pdf ] || { echo "MISSING: ies-report.pdf"; missing=1; }
if [ "$missing" -ne 0 ]; then
  echo "::error::publish dir incomplete; aborting before replacing gh-pages"
  exit 1
fi
echo "publish dir complete ($(git ls-files schemas/ | wc -l) schema files + PDF)"

python3 -B scripts/verify_pdf.py --public-root public

[ -s build/ies_accelerator.pdf ] || { echo "::error::build/ies_accelerator.pdf missing or empty"; exit 1; }
[ -s public/ies-report.pdf ] || { echo "::error::public/ies-report.pdf missing or empty"; exit 1; }
cmp -s build/ies_accelerator.pdf public/ies-report.pdf || {
  echo "::error::build/ies_accelerator.pdf and public/ies-report.pdf differ"
  exit 1
}

python3 -B scripts/verify_publication.py \
  --public-root public \
  --combined-md build/ies_combined.md \
  --manifest build/public-manifest.txt
python3 -B scripts/verify_publication.py --self-test
