# A/JUNCTION: 공통좌표

아주대학교 중앙도서관 미디어월을 위해 제작한 **Manim 기반 미디어아트 모션그래픽**입니다.

서로 다른 단과대와 학문 분야를 기하학적 형태와 움직임으로 시각화하고, 각자의 방향으로 전개되던 형상들이 도서관이라는 **공통좌표(Junction)** 에서 교차·연결되어 마지막에는 아주대학교 심볼로 결집하도록 구성했습니다.

> **아주대학교 중앙도서관 미디어월 공모전 우수상 수상작**

## Project

- **Title:** A/JUNCTION: 공통좌표
- **Format:** 5200 × 1664 media-wall motion graphic
- **Runtime:** approximately 1m 55s
- **Tool:** Python / Manim Community
- **Style:** textless geometric motion art
- **Concept:** Library as a common coordinate where different academic fields intersect

## Visual Structure

1. College of Engineering
2. College of Advanced ICT Convergence
3. College of Software Convergence
4. College of Natural Sciences
5. College of Advanced Bio Convergence
6. College of Pharmacy
7. College of Medicine
8. College of Nursing
9. College of Business Administration
10. College of Social Sciences
11. College of Humanities
12. Division of International Studies
13. Dasan University College / Open Major
14. Final geometric assembly into the Ajou University symbol

## Source

The main Manim source is located at:

`src/ajou_field_v2_manim.py`

Render scripts are included for preview and media-wall resolution.

## Render

### Preview

```bash
./render_preview.sh
```

### Final

```bash
./render_final.sh
```

Requirements: Manim Community 0.20.x, NumPy, Pillow, and FFmpeg.

## Media

A lightweight preview is included in the repository.  
The full 5200×1664 exhibition master is larger than GitHub's normal file limit, so it should be distributed through Git LFS or a release asset rather than committed as a normal Git blob.

---

Created for the Ajou University Library media wall.
