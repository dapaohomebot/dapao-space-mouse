#!/bin/bash
# Export all printable parts as individual STL files
# Requires OpenSCAD installed locally
# Usage: ./export_stls.sh

set -e

SCAD_FILE="space_mouse.scad"
OUTPUT_DIR="stl"
mkdir -p "$OUTPUT_DIR"

PARTS=(
    "base_plate"
    "base_ring"
    "body"
    "top_cap"
    "button_top_left"
    "button_top_right"
    "button_side"
    "joystick_coupler"
)

echo "Exporting STL files from $SCAD_FILE..."
echo "Output directory: $OUTPUT_DIR/"
echo ""

for part in "${PARTS[@]}"; do
    echo "  Rendering: $part..."
    openscad -o "$OUTPUT_DIR/${part}.stl" \
        -D "RENDER_PART=\"$part\"" \
        -D "\$fn=120" \
        "$SCAD_FILE"
    echo "    → $OUTPUT_DIR/${part}.stl"
done

echo ""
echo "Done! All STL files exported to $OUTPUT_DIR/"
echo ""
echo "Print settings:"
echo "  Layer height: 0.2mm"
echo "  Infill: 20%"
echo "  Material: PLA or PETG"
echo "  Supports: needed for base_ring (side button overhangs)"
