#!/usr/bin/env bash
set -euo pipefail

INPUT_MD="${1:-docs/tax_calculator_cfg_mermaid.md}"
OUT_DIR="docs/build"
mkdir -p "$OUT_DIR"

if [[ ! -f "$INPUT_MD" ]]; then
  echo "Input file not found: $INPUT_MD" >&2
  exit 1
fi

if command -v mmdc >/dev/null 2>&1; then
  MMDC=(mmdc)
elif command -v npx >/dev/null 2>&1; then
  MMDC=(npx -y @mermaid-js/mermaid-cli mmdc)
else
  echo "Mermaid CLI missing. Install one of:" >&2
  echo "  npm i -g @mermaid-js/mermaid-cli" >&2
  echo "or install Node.js so npx is available." >&2
  exit 1
fi

TMP_MMD="$(mktemp)"
awk '
  /^```mermaid[[:space:]]*$/ { in_block=1; next }
  /^```[[:space:]]*$/ && in_block { in_block=0; exit }
  in_block { print }
' "$INPUT_MD" > "$TMP_MMD"

if [[ ! -s "$TMP_MMD" ]]; then
  echo "No mermaid block found in $INPUT_MD" >&2
  rm -f "$TMP_MMD"
  exit 1
fi

"${MMDC[@]}" -i "$TMP_MMD" -o "$OUT_DIR/tax_calculator_cfg.svg"
"${MMDC[@]}" -i "$TMP_MMD" -o "$OUT_DIR/tax_calculator_cfg.png"

rm -f "$TMP_MMD"
echo "Built:" 
echo "  $OUT_DIR/tax_calculator_cfg.svg"
echo "  $OUT_DIR/tax_calculator_cfg.png"
