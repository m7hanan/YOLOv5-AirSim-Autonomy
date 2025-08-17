# YOLOv5 + AirSim Autonomy

Real‑time person & car detection with YOLOv5 inside Microsoft AirSim, plus simple waypoint navigation and basic collision avoidance.

[▶️ Watch the demo on YouTube](https://youtu.be/SuTeEVTpxuw?si=joeSaWKcEFA3DiKz)

![Drone Object Detection Demo](assets/drone_object_detection.gif)


---

## Features
- ✅ YOLOv5s (Torch Hub) for fast inference
- ✅ AirSim multirotor control: takeoff, waypoint navigation, slow landing
- ✅ Simple vision‑based obstacle check in image center region
- ✅ Optional headless mode (no GUI)
- ✅ Scripted recording to MP4

## Quickstart
```bash
conda create -n yolo-airsim python=3.10 -y
conda activate yolo-airsim
pip install -r requirements.txt
python scripts/run_demo.py --config configs/default.yaml
