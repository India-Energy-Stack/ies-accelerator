#!/usr/bin/env python3
"""Build the Word copies of the Propose a Schema hand-outs.

  .github/templates/use-case-overview.md -> .github/templates/use-case-overview.docx
  before-you-propose.md                  -> before-you-propose.docx

The Markdown files are the source of truth; each .docx sits next to its
source so the GitBook pages can offer a one-click download. Rerun this
whenever either source changes, and commit the .md and .docx together.

Reuses the reference-docx styling of scripts/build_docx.py so the files
match the Technical Reference .docx.

Usage:  python3 scripts/build_template_docx.py
        (or: make template-docx)
"""

import pathlib
import re
import shutil
import subprocess
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import build_docx as bd

ROOT = bd.ROOT
GITHUB_BLOB = "https://github.com/India-Energy-Stack/ies-accelerator/blob/main/"
GITBOOK = "https://india-energy-stack.gitbook.io/docs/"

# Relative links die once the file leaves the repo. These pages have known
# GitBook URLs; any other relative link falls back to its GitHub view.
GITBOOK_PAGES = {
    "propose-a-schema.md": GITBOOK + "propose-a-schema",
    "schemas-ies/taxonomy.md": GITBOOK + "schemas/taxonomy",
}

TEMPLATE_PREAMBLE = f"""\
> **India Energy Stack — use-case overview template.** Use it to write the
> **concept note** that accompanies a schema proposal. Fill in the slots, share
> the finished document as a public link (a Google Doc or OneDrive file anyone
> with the link can view), and paste that link into the *Concept note (link)*
> field of the Propose a Schema form. The canonical version of this template is
> [on GitHub]({GITHUB_BLOB}.github/templates/use-case-overview.md); if the two
> ever differ, GitHub wins.

"""

# (source, preamble, compact) — a reader who downloads the .docx has lost the
# page that told them what it is for, so the template gets a note saying so.
# compact: smaller headings, so the checklist stays a one-pager.
DOCS = [
    (ROOT / ".github" / "templates" / "use-case-overview.md", TEMPLATE_PREAMBLE, False),
    (ROOT / "before-you-propose.md", "", True),
]

# Web-only lines — the page's own "download as Word" link and its closing
# "Ready? → form" footer — are noise inside the Word file itself.
WEB_ONLY = re.compile(
    r"^.*Download this .* as Word \(\.docx\).*\n\n?|^---\n\nReady\?.*\n?\Z", re.M
)

LINK = re.compile(r"\]\(([^)\s]+)\)")


def absolutize(md: str, src: pathlib.Path) -> str:
    def fix(m: re.Match) -> str:
        target = m.group(1)
        if re.match(r"[a-z]+:", target) or target.startswith("#"):
            return m.group(0)
        path, _, anchor = target.partition("#")
        rel = (src.parent / path).resolve().relative_to(ROOT).as_posix()
        url = GITBOOK_PAGES.get(rel, GITHUB_BLOB + rel)
        return f"]({url}{'#' + anchor if anchor else ''})"

    return LINK.sub(fix, md)


def compact_reference(reference: pathlib.Path) -> pathlib.Path:
    """The shared reference docx with Heading 1/2 shrunk (20pt -> 16pt,
    16pt -> 12pt) and tighter space above them."""
    out = reference.with_name("docx_reference_compact.docx")
    with zipfile.ZipFile(reference) as zin, zipfile.ZipFile(
        out, "w", zipfile.ZIP_DEFLATED
    ) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            if item.filename == "word/styles.xml":
                text = data.decode("utf-8")
                for sid, old, new in (("Heading1", "40", "32"), ("Heading2", "32", "24")):
                    text = re.sub(
                        rf'(w:styleId="{sid}">.*?)<w:sz w:val="{old}" />\s*<w:szCs w:val="{old}" />',
                        rf'\1<w:sz w:val="{new}" /><w:szCs w:val="{new}" />',
                        text,
                        count=1,
                        flags=re.DOTALL,
                    )
                for sid, old, new in (
                    ("Heading1", 'w:before="360" w:after="80"', 'w:before="0" w:after="80"'),
                    ("Heading2", 'w:before="160" w:after="80"', 'w:before="100" w:after="40"'),
                ):
                    text = re.sub(
                        rf'(w:styleId="{sid}">.*?)<w:spacing {old} />',
                        rf'\1<w:spacing {new} />',
                        text,
                        count=1,
                        flags=re.DOTALL,
                    )
                data = text.encode("utf-8")
            zout.writestr(item, data)
    return out


def main() -> int:
    if shutil.which("pandoc") is None:
        print("error: pandoc not found. Install with: brew install pandoc", file=sys.stderr)
        return 1

    bd.bp.BUILD.mkdir(exist_ok=True)
    reference = bd.make_reference_docx()
    compact = compact_reference(reference)
    for src, preamble, is_compact in DOCS:
        out = src.with_suffix(".docx")
        staged = bd.bp.BUILD / ("docx-handout-" + src.name)
        body = WEB_ONLY.sub("", src.read_text())
        staged.write_text(preamble + absolutize(body, src))
        subprocess.run(
            [
                "pandoc",
                str(staged),
                "--output=" + str(out),
                "--from=markdown-task_lists",
                "--metadata",
                "lang=en-IN",
                "--reference-doc=" + str(compact if is_compact else reference),
            ],
            check=True,
        )
        print(f"wrote {out.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
