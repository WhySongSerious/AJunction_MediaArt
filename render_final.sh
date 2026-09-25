#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
# Exact Ajou Library media-wall resolution.
manim --disable_caching --resolution 5200,1664 --frame_rate 24 --format mp4 src/ajou_field_v2_manim.py AjouFieldV2
