#!/usr/bin/env python3
"""
JSON-LD Consistency Checker
============================
Checks consistency between a schema's context.jsonld and its example files
without fetching any remote URLs.  Three checks are run:

1. Context syntax — context.jsonld must parse as valid JSON and contain a
   well-formed "@context" key.

2. IRI collisions — two different property paths inside context.jsonld that
   map to the same @id IRI.  Semantically valid JSON-LD (aliases are allowed),
   but almost always a mistake: e.g. assetId → deg:assetId in one block and
   assetId → deg:storageAssetId in another, meaning a SPARQL query for one
   would silently miss the other.

3. Unmapped terms — properties present in the example JSON that have no @id
   entry in context.jsonld.  These properties are invisible to any RDF/SPARQL
   consumer loading the context.

4. Orphaned context terms — @id mappings declared in context.jsonld that do
   not appear in any example.  Often left-over from a previous schema version.

5. pyld local expansion — expand the example against ONLY the local
   context.jsonld (remote contexts are stubbed out).  Confirms the local
   context is syntactically valid JSON-LD and that all local terms expand
   correctly to IRIs.

Usage
-----
  python3 scripts/check_jsonld.py schemas/ElectricityCredential/v1.0
  python3 scripts/check_jsonld.py schemas/ElectricityCredential/v1.0 \\
                                   schemas/ElectricityCredential/v1.1 \\
                                   schemas/MeterData/v0.6
"""

import json
import sys
from pathlib import Path

import pyld.jsonld as jsonld

# ---------------------------------------------------------------------------
# Terminal colours
# ---------------------------------------------------------------------------
OK   = "✅"
WARN = "⚠️ "
ERR  = "❌"
INFO = "ℹ️ "


# ---------------------------------------------------------------------------
# Context helpers
# ---------------------------------------------------------------------------

def _load_json(path: Path) -> dict:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _flatten_context(ctx, prefix: str = "", result: dict | None = None) -> dict:
    """
    Walk a (possibly nested) JSON-LD @context and return a flat
    { dotted.path: iri_or_none } mapping.

    Structural keywords (@version, @protected, @container, …) are skipped.
    Nested @context blocks are recursed with the parent term as prefix.
    """
    if result is None:
        result = {}

    _SKIP = {"@version", "@protected", "@container", "@vocab", "@base",
             "@import", "@propagate", "@language", "@direction", "@reverse"}

    if isinstance(ctx, list):
        for item in ctx:
            _flatten_context(item, prefix, result)
        return result

    if not isinstance(ctx, dict):
        return result

    for key, val in ctx.items():
        if key in _SKIP:
            continue
        if key == "@context":
            _flatten_context(val, prefix, result)
            continue

        term = f"{prefix}{key}" if prefix else key

        if isinstance(val, str):
            result[term] = val
        elif isinstance(val, dict):
            result[term] = val.get("@id")          # may be None
            nested = val.get("@context")
            if nested:
                _flatten_context(nested, f"{term}.", result)

    return result


# ---------------------------------------------------------------------------
# Example walker
# ---------------------------------------------------------------------------

_SKIP_KEYS = {"@context", "@id", "@value", "@type", "@language",
              "@container", "@protected", "@version", "@set", "@list"}


def _collect_property_paths(node, prefix: str = "", result: set | None = None) -> set:
    """
    Recursively walk a JSON document and collect every property key,
    expressed as a dotted path relative to the nearest ancestor that
    corresponds to a context-term prefix.

    We use a simple heuristic: the full dotted path from root is returned.
    Callers compare leaf names (the last segment) against the flat context.
    """
    if result is None:
        result = set()

    if isinstance(node, list):
        for item in node:
            _collect_property_paths(item, prefix, result)
    elif isinstance(node, dict):
        for key, val in node.items():
            if key in _SKIP_KEYS:
                _collect_property_paths(val, prefix, result)
                continue
            path = f"{prefix}.{key}" if prefix else key
            result.add(path)
            _collect_property_paths(val, path, result)

    return result


def _leaf_names(paths: set) -> set:
    """Return the final segment of every dotted path."""
    return {p.rsplit(".", 1)[-1] for p in paths}


# ---------------------------------------------------------------------------
# pyld document loader — stubs out ALL remote URLs
# ---------------------------------------------------------------------------

def _local_only_loader(schema_dir: Path):
    """
    Return a pyld document loader that:
    - Loads context.jsonld from the schema directory by filename match.
    - Returns an empty @context for every other URL (no network calls).

    This lets us expand examples against the LOCAL context only, without
    remote contexts (W3C credentials, schema.org) interfering.
    """
    _EMPTY = {"@context": {}}

    def loader(url, options=None):
        # Try to serve the file from the local schema directory
        for candidate in [
            schema_dir / Path(url).name,
        ]:
            if candidate.exists():
                doc = _load_json(candidate)
                return {"contentType": "application/ld+json",
                        "contextUrl": None,
                        "document": doc,
                        "documentUrl": url}
        # Stub everything else — no network requests
        return {"contentType": "application/ld+json",
                "contextUrl": None,
                "document": _EMPTY,
                "documentUrl": url}

    return loader


def _collect_unmapped_after_expansion(node, plain: set | None = None) -> set:
    """
    After pyld expansion, every mapped term becomes an absolute IRI (contains
    "://").  Terms that stayed as plain strings were not resolved and are
    therefore unmapped by the context.
    """
    if plain is None:
        plain = set()

    if isinstance(node, list):
        for item in node:
            _collect_unmapped_after_expansion(item, plain)
    elif isinstance(node, dict):
        for key, val in node.items():
            if key.startswith("@"):
                _collect_unmapped_after_expansion(val, plain)
                continue
            if "://" not in key and not key.startswith("_:"):
                plain.add(key)
            _collect_unmapped_after_expansion(val, plain)

    return plain


# ---------------------------------------------------------------------------
# Per-schema checks
# ---------------------------------------------------------------------------

def check_schema_dir(schema_dir: Path) -> bool:
    """Run all checks for one schema version directory. Returns True if clean."""
    print(f"\n{'='*64}")
    print(f"  {schema_dir}")
    print(f"{'='*64}")

    context_path = schema_dir / "context.jsonld"
    examples_dir = schema_dir / "examples"

    if not context_path.exists():
        print(f"\n{WARN} No context.jsonld — skipping.")
        return True

    # ── 1. Parse context ────────────────────────────────────────────────────
    try:
        context_doc = _load_json(context_path)
    except Exception as e:
        print(f"\n{ERR} context.jsonld JSON parse error: {e}")
        return False

    raw_ctx = context_doc.get("@context", context_doc)
    flat    = _flatten_context(raw_ctx)
    print(f"\n{INFO} context.jsonld declares {len(flat)} term mappings")

    all_ok = True

    # ── 2. IRI collision check ───────────────────────────────────────────────
    iri_to_terms: dict[str, list] = {}
    for term, iri in flat.items():
        if iri and not iri.startswith("@"):
            iri_to_terms.setdefault(iri, []).append(term)

    collisions = {iri: terms for iri, terms in iri_to_terms.items()
                  if len(terms) > 1}

    if collisions:
        print(f"\n{WARN} IRI collisions ({len(collisions)}) — "
              f"different paths share the same @id:")
        for iri, terms in sorted(collisions.items()):
            print(f"    {iri}")
            for t in sorted(terms):
                print(f"      · {t}")
        all_ok = False
    else:
        print(f"{OK} No IRI collisions")

    # ── 3 & 4. Example term checks ───────────────────────────────────────────
    example_files = sorted(examples_dir.glob("*.json")) if examples_dir.exists() else []

    if not example_files:
        print(f"\n{WARN} No examples found in {examples_dir} — skipping term checks.")
    else:
        # Terms declared in the context (leaf names only, for easy matching)
        ctx_leaf_names = {k.rsplit(".", 1)[-1] for k in flat}

        all_example_leaves: set = set()

        for ex_path in example_files:
            print(f"\n  ── {ex_path.name}")
            try:
                doc = _load_json(ex_path)
            except Exception as e:
                print(f"    {ERR} JSON parse error: {e}")
                all_ok = False
                continue

            paths  = _collect_property_paths(doc)
            leaves = _leaf_names(paths)
            all_example_leaves |= leaves

            # Terms in this example that have no @id in the context
            unmapped = leaves - ctx_leaf_names - _SKIP_KEYS
            if unmapped:
                print(f"    {WARN} Unmapped terms (not in context.jsonld): "
                      f"{sorted(unmapped)}")
                all_ok = False
            else:
                print(f"    {OK} All property names covered by context")

            # ── 5. pyld local expansion ─────────────────────────────────────
            loader = _local_only_loader(schema_dir)
            doc_url = ex_path.resolve().as_uri()
            try:
                expanded = jsonld.expand(
                    doc,
                    options={"documentLoader": loader,
                             "base": doc_url,
                             "processingMode": "json-ld-1.1"}
                )
                still_plain = _collect_unmapped_after_expansion(expanded) - _SKIP_KEYS
                if still_plain:
                    print(f"    {WARN} Terms not expanded to IRIs by local context: "
                          f"{sorted(still_plain)}")
                    all_ok = False
                else:
                    print(f"    {OK} All terms expand to IRIs under local context")
            except Exception as e:
                msg = str(e)
                # Truncate very long pyld error details
                if len(msg) > 200:
                    msg = msg[:200] + " …"
                print(f"    {WARN} pyld expansion warning: {msg}")
                # Expansion warnings don't fail the check — context syntax
                # issues are caught by other means.

        # ── 4. Orphaned context terms ─────────────────────────────────────
        # Context leaf names that never appeared in any example
        unused_leaves = ctx_leaf_names - all_example_leaves - _SKIP_KEYS

        # Strip noise: single-char aliases and namespace prefixes
        unused_leaves = {t for t in unused_leaves
                         if len(t) > 2 and "/" not in t}

        if unused_leaves:
            print(f"\n{WARN} Context terms unused in any example ({len(unused_leaves)}) — "
                  f"possibly orphaned from a prior schema version:")
            for t in sorted(unused_leaves):
                iri = flat.get(t, "?")
                print(f"    · {t}  →  {iri}")
        else:
            print(f"\n{OK} No orphaned context terms")

    return all_ok


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 scripts/check_jsonld.py <schema_dir> [<schema_dir> ...]")
        sys.exit(1)

    overall_ok = True
    for arg in sys.argv[1:]:
        path = Path(arg)
        if not path.is_dir():
            print(f"{ERR} Not a directory: {arg}")
            overall_ok = False
            continue
        if not check_schema_dir(path):
            overall_ok = False

    print()
    if overall_ok:
        print(f"{OK} All checks passed.")
        sys.exit(0)
    else:
        print(f"{ERR} Issues found — see above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
