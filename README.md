# AuraSight

**A proof-of-concept for AR-assisted surgical tool tracking — real-time computer vision on a live camera feed, built as a software-first, hardware-agnostic prototype.**

AuraSight overlays a live medical-style HUD on a video feed, tracking hands and surgical tools in real time. It's an early-stage exploration into low-cost surgical navigation aids, aimed at markets where legacy optical navigation systems are too expensive to deploy widely.

---

## What it does today

- **Tool detection** — YOLOv8 (`yolov8n.pt`) identifies surgical tools (currently knife/scissors classes) in the live frame and draws bounding-box callouts with confidence scores.
- **Hand tracking** — MediaPipe HandLandmarker tracks both hands, drawing landmark skeletons and labeling left/right in real time.
- **Glove detection** — an HSV-based skin-tone heuristic checks the region around each detected hand to flag whether a surgical glove is likely being worn.
- **Tool-to-hand association** — matches detected tools to the nearest tracked hand using bounding-box proximity, so the HUD can show which hand is holding what.
- **Live HUD** — a medical-grade heads-up display (status panel, glove panel, confidence bar, FPS counter) rendered directly on the video feed with OpenCV.
- **GPU-aware inference** — automatically runs on CUDA if available, falls back to CPU otherwise.

This runs on a standard webcam feed today — no specialized capture hardware required.

## Tech stack

- `ultralytics` (YOLOv8) — object detection
- `mediapipe` — hand landmark tracking
- `opencv-python` — video capture, rendering, HSV color analysis
- `torch` / `torchvision` — inference backend

## Getting started

```bash
git clone https://github.com/Aayushg416/AuraSight.git
cd AuraSight
pip install -r requirements.txt
python main.py
```

Requires a webcam. Press `Q` to quit the live view.

## Repository contents

| File | Purpose |
|---|---|
| `main.py` | Core application — detection, tracking, HUD rendering |
| `requirements.txt` | Python dependencies |
| `yolov8n.pt` | YOLOv8 nano weights used for tool detection |
| `hand_landmarker.task` | MediaPipe hand landmark model |
| `AuraSight_Startup_Plan.md` | Business/market plan for the concept |
| `AuraSight Surgical.pdf`, `AuraSight.pptx` | Pitch materials |

---

## Roadmap / vision —  yet to be implemented

The current build is a single-camera detection-and-overlay prototype. The larger product vision this project is working toward includes:

- **SLAM-based spatial tracking** for stable 3D registration of tools relative to the surgical field, instead of frame-by-frame 2D detection
- **DICOM ingestion and ICP (Iterative Closest Point) registration** to align pre-operative CT/MRI scans onto the live operative field — the core "AR surgical navigation" capability
- **Deployment to embedded hardware** (e.g. NVIDIA Jetson Orin) to move off a laptop and hit real-time inference budgets in an OR-viable form factor, with a target of 30+ FPS end-to-end
- **Sub-millimeter tool tracking accuracy** and AI-driven proximity alerts, once spatial registration is in place
- **India-first regulatory path**, targeting CDSCO Class B classification, positioned against legacy optical navigation systems that carry significantly higher capital cost

None of these are in the current codebase — they're the next build phases. Flagging this explicitly so the README doesn't overstate what `main.py` does today.

## Status

Early prototype / proof-of-concept. Not validated for clinical use.
