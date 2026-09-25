# A/JUNCTION: 공통좌표

> **2026 아주대학교 중앙도서관 미디어월 콘텐츠 공모전 우수상 수상작**

**A/JUNCTION: 공통좌표**는 아주대학교 중앙도서관을 서로 다른 학문이 만나고 교차하는 하나의 **Junction**으로 해석한 미디어아트 모션그래픽입니다.

공학, ICT, 소프트웨어, 자연과학, 바이오, 의·약학, 간호, 경영, 사회과학, 인문, 국제학 등 서로 다른 학문 분야를 각기 다른 **점·선·면·파동·네트워크·궤도**의 움직임으로 형상화했습니다. 각자의 방향으로 전개되던 요소들은 마지막 장면에서 하나의 좌표로 수렴해 **아주대학교 심볼**을 완성합니다.

---

## 🏆 Award

**2026 아주대학교 중앙도서관 미디어월 콘텐츠 공모전 — 우수상**

실제 중앙도서관 미디어월 상영 규격을 고려해 **5200 × 1664**의 초광폭 화면을 기준으로 제작했습니다.

> 수상 상장 이미지는 `assets/award_certificate.png`에 추가할 예정입니다.

---

## 🎬 Final Artwork

| 항목 | 내용 |
|---|---|
| 작품명 | **A/JUNCTION: 공통좌표** |
| 형식 | Media Art / Motion Graphics |
| 제작 도구 | **Python, Manim Community, FFmpeg** |
| 최종 해상도 | **5200 × 1664** |
| 러닝타임 | **약 1분 55초** |
| 프레임레이트 | 24 fps |
| 전시 환경 | 아주대학교 중앙도서관 미디어월 |
| 결과 | **우수상 수상** |

### Exhibition Master

최종 전시본은 영상 후반부로 갈수록 음악이 고조되고, 마지막 A/J 심볼 결집 장면에서 클라이맥스가 오도록 사운드를 재편집한 버전입니다.

```text
A_JUNCTION_공통좌표_무명음악_최종.mp4
```

> GitHub 일반 파일 업로드 제한을 넘는 고해상도 마스터이므로 Git LFS 또는 GitHub Release asset으로 관리하는 것을 권장합니다.

---

## 💡 Concept

도서관은 특정 전공만을 위한 공간이 아니라 서로 다른 학문을 공부하는 학생들이 동시에 머무는 장소입니다.

이 작품은 그 공간을 **공통좌표(Common Coordinate)** 로 바라봅니다.

- 서로 다른 학문은 각각 고유한 형태와 운동 법칙을 가진다.
- 각 장면은 특정 단과대의 사고방식과 대상을 추상적 기하학으로 변환한다.
- 장면과 장면은 단절되지 않고 하나의 흐름으로 이어진다.
- 마지막에는 모든 학문적 파편이 하나의 아주대학교 심볼로 결집한다.

작품명 **A/JUNCTION**은 **AJOU**의 `A/J`와 서로 다른 흐름이 만나는 **Junction**의 의미를 결합한 이름입니다.

---

## 🧭 Visual Timeline

| Timeline | Academic Field | Visual Motif |
|---|---|---|
| 00:00–00:09 | 공과대학 | 기계 구조, 결정 격자, 트러스, 유체 흐름 |
| 00:09–00:17 | 첨단ICT융합대학 | 회로, 반도체, 신호, 센서 파동 |
| 00:17–00:25 | 소프트웨어융합대학 | 데이터, 보안, AI 네트워크 |
| 00:25–00:34 | 자연과학대학 | 좌표, 파동, 원자, 세포 |
| 00:34–00:42 | 첨단바이오융합대학 | DNA, 단백질, 바이오 네트워크 |
| 00:42–00:50 | 약학대학 | 캡슐, 분자, 수용체, 확산 |
| 00:50–00:58 | 의과대학 | 인체 단면, 진단 스캔, 조직 |
| 00:58–01:06 | 간호대학 | 환자 침상, 생체신호, IV, 돌봄 네트워크 |
| 01:06–01:14 | 경영대학 | 의사결정, 데이터 그래프, 시장 |
| 01:14–01:22 | 사회과학대학 | 개인과 집단, 제도, 사회 연결 |
| 01:22–01:30 | 인문대학 | 책, 언어, 음성, 시간축 |
| 01:30–01:38 | 국제학부 | 지구, 교류 궤도, 국제 연결 |
| 01:38–01:45 | 다산학부대학 / 자유전공 | 선택과 분기, 학문 경로 |
| 01:45–01:55 | **Convergence** | 모든 형상이 수렴해 Ajou Symbol 완성 |

---

## 🛠 Implementation

### Manim

작품의 핵심 애니메이션은 **Manim Community**를 사용해 코드 기반으로 제작했습니다.

단순히 정해진 영상을 편집하는 방식보다, 위치·회전·스케일·궤적·파동·네트워크 연결을 수학적으로 제어할 수 있다는 점을 활용했습니다.

메인 소스:

```text
src/ajou_field_v2_manim.py
```

### Media-wall Composition

일반적인 16:9 화면이 아닌 **5200 × 1664** 초광폭 비율이기 때문에 화면 중앙에만 오브젝트가 몰리지 않도록 장면별로 좌우 공간을 적극적으로 사용했습니다.

### Sound

최종 전시본은 음악을 단순히 앞에서부터 자르지 않고 영상 구조에 맞춰 재편집했습니다. 초반에는 비교적 절제하고, 후반부로 갈수록 밀도를 높여 마지막 심볼 결집 장면이 음악적으로도 클라이맥스가 되도록 구성했습니다.

---

## 📁 Repository Structure

```text
AJunction_MediaArt/
├─ README.md
├─ requirements.txt
├─ render_preview.sh
├─ render_final.sh
├─ src/
│  └─ ajou_field_v2_manim.py
├─ assets/
│  ├─ award_certificate.png   # award certificate
│  ├─ ajou_logo_symbol.png    # Ajou symbol asset
│  └─ storyboard.png          # visual overview
└─ media/
   └─ master/
      └─ A_JUNCTION_공통좌표_무명음악_최종.mp4
```

---

## ▶️ Render

### Install

```bash
pip install -r requirements.txt
```

FFmpeg is also required.

### Preview

```bash
./render_preview.sh
```

### 5200 × 1664 Final Render

```bash
./render_final.sh
```

---

## 🎯 What I Focused On

이 프로젝트에서 가장 중요하게 본 것은 **전공을 아이콘 하나로 직접 설명하는 것이 아니라, 학문의 성격 자체를 움직임의 규칙으로 번역하는 것**이었습니다.

예를 들어 소프트웨어는 데이터와 네트워크, 자연과학은 좌표와 파동, 바이오는 DNA와 생명 구조, 의학은 진단과 조직, 간호는 생체신호와 돌봄의 연결로 구분했습니다. 이렇게 만들어진 서로 다른 시각 언어가 마지막에 하나의 상징으로 결집하면서 작품 전체의 메시지를 완성합니다.

---

## 👤 Creator

**Song Jaehyeok (송재혁)**  
Digital Media / Ajou University

---

### A/JUNCTION

**Different disciplines. One common coordinate.**
