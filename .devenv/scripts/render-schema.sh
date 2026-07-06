#!/usr/bin/env bash
# Converts schema.mermaid to SVG and/or PNG via Graphviz (dot).
#
# Pipeline:
#   schema.mermaid → mermaid-to-dot.py → schema.dot → dot → schema.svg / schema.png
#
# Usage: render-schema.sh [--svg] [--png] [--out DIR]
#
# Options:
#   --svg      Render to SVG (default if neither --svg nor --png given)
#   --png      Render to PNG (requires dot with PNG support)
#   --out DIR  Output directory (default: same directory as schema.mermaid)
#
# Requirements: python3, graphviz (dot)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCHEMA_MERMAID="$REPO_ROOT/docs/documentation/reference/db-schema/schema.mermaid"
SCHEMA_DOT="$REPO_ROOT/docs/documentation/reference/db-schema/schema.dot"
CONVERTER="$SCRIPT_DIR/mermaid-to-dot.py"

DO_SVG=false
DO_PNG=false
OUT_DIR=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --svg) DO_SVG=true ;;
    --png) DO_PNG=true ;;
    --out) OUT_DIR="$2"; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
  shift
done

if ! $DO_SVG && ! $DO_PNG; then
  DO_SVG=true
fi

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="$(dirname "$SCHEMA_MERMAID")"
fi

# ── dependency checks ──────────────────────────────────────────────────────────
if ! command -v python3 &>/dev/null; then
  echo "Error: python3 not found." >&2; exit 1
fi
if ! command -v dot &>/dev/null; then
  echo "Error: graphviz 'dot' not found. Install with: brew install graphviz" >&2; exit 1
fi

# ── step 1: convert mermaid → dot ─────────────────────────────────────────────
echo "Converting schema.mermaid → schema.dot"
python3 "$CONVERTER" "$SCHEMA_MERMAID" "$SCHEMA_DOT"

# ── step 2: render dot → output format(s) ─────────────────────────────────────
render() {
  local fmt="$1"
  local out="$OUT_DIR/schema.$fmt"
  echo "Rendering $fmt → $out"
  dot "-T$fmt" "$SCHEMA_DOT" -o "$out"
}

$DO_SVG && render svg
$DO_PNG && render png

echo "Done."
