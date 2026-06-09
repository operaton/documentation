#!/usr/bin/env bash
# Converts schema.mermaid to SVG and/or PNG using mermaid-cli (mmdc via npx).
#
# Usage: render-schema.sh [--svg] [--png] [--out DIR]
#
# Options:
#   --svg      Render to SVG (default if neither --svg nor --png given)
#   --png      Render to PNG
#   --out DIR  Output directory (default: same directory as schema.mermaid)
#
# Requirements: Node.js with npx available in PATH

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
SCHEMA="$REPO_ROOT/docs/documentation/reference/db-schema/schema.mermaid"
CSS="$SCRIPT_DIR/schema-theme.css"

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

# Default to SVG if nothing specified
if ! $DO_SVG && ! $DO_PNG; then
  DO_SVG=true
fi

if [[ -z "$OUT_DIR" ]]; then
  OUT_DIR="$(dirname "$SCHEMA")"
fi

if ! command -v npx &>/dev/null; then
  echo "Error: npx not found. Install Node.js to use this script." >&2
  exit 1
fi

CSS_ARGS=()
if [[ -f "$CSS" ]]; then
  CSS_ARGS=(-C "$CSS")
fi

render() {
  local fmt="$1"
  local out="$OUT_DIR/schema.$fmt"
  echo "Rendering $fmt → $out"
  npx --yes @mermaid-js/mermaid-cli \
    -i "$SCHEMA" \
    -o "$out" \
    "${CSS_ARGS[@]}"
}

$DO_SVG && render svg
$DO_PNG && render png

echo "Done."
