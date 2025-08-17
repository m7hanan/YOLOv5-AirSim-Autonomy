from dataclasses import dataclass, field
from pathlib import Path
import argparse
import yaml
from typing import List


@dataclass
class AirSimCfg:
    ip: str = "127.0.0.1"
    port: int = 41451
    vehicle_name: str = ""


@dataclass
class VisionCfg:
    model: str = "yolov5s"
    classes: List[int] = field(default_factory=lambda: [0, 2])
    conf: float = 0.6
    iou: float = 0.45
    headless: bool = False


@dataclass
class NavCfg:
    speed: float = 3.0
    waypoints: List[List[float]] = field(default_factory=lambda: [
        [10, 10, -10],
        [10, 12, -20.81],
        [15, 60, -4],
        [22, 29, -13.88]
    ])


@dataclass
class RecordingCfg:
    output: str = "videos/demo.mp4"
    fps: int = 30


@dataclass
class Config:
    airsim: AirSimCfg = AirSimCfg()
    vision: VisionCfg = VisionCfg()
    nav: NavCfg = NavCfg()
    recording: RecordingCfg = RecordingCfg()


def load_config() -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    args, _ = parser.parse_known_args()

    cfg_data = {}
    config_path = Path(args.config)
    if config_path.exists():
        with open(config_path, "r") as f:
            cfg_data = yaml.safe_load(f) or {}

    def merge(dataclass_type, values):
        obj = dataclass_type()
        for k, v in values.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        return obj

    return Config(
        airsim=merge(AirSimCfg, cfg_data.get("airsim", {})),
        vision=merge(VisionCfg, cfg_data.get("vision", {})),
        nav=merge(NavCfg, cfg_data.get("nav", {})),
        recording=merge(RecordingCfg, cfg_data.get("recording", {})),
    )
