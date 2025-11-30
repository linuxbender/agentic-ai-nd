#!/usr/bin/env bash
set -euo pipefail
# Render Mermaid diagram to PNG and SVG using mermaid-cli (requires Node.js)
# Usage: ./render_diagram.sh workflow.mmd

INPUT=${1:-workflow.mmd}
BASENAME=$(basename "$INPUT" .mmd)

if ! command -v mmdc >/dev/null 2>&1; then
  echo "mermaid-cli (mmdc) not found. Install with: npm i -g @mermaid-js/mermaid-cli"
  exit 1
fi

mmdc -i "$INPUT" -o "$BASENAME.png" -b light
mmdc -i "$INPUT" -o "$BASENAME.svg" -b light

echo "Rendered: $BASENAME.png and $BASENAME.svg"

