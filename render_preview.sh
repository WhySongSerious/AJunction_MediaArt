#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
manim --disable_caching --resolution 1600,512 --frame_rate 24 --format mp4 src/ajou_field_v2_manim.py AjouFieldV2
