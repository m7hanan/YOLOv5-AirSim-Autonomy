from dataclasses import dataclass
from pathlib import Path
import argparse
import yaml


@dataclass
class AirSimCfg:
    ip: str = "127.0.0.1"
    port: int = 41451
    vehicle_name: str = ""


@dataclass
class VisionCfg:
    model: str = "yolov5s"
    classes: list[int] = None
    conf: float = 0.6
    iou: float = 0.45
    headless: bool = False


@dataclass
class NavCfg:
    speed: float = 3.0
    waypoints: list[list[float]] = None


@dataclass
class RecordingCfg:
    output: str = "videos/demo.mp4"
    fps: int = 30


@dataclass
class Config:
    airsim: AirSimCfg = AirSimCfg()
    vision: VisionCfg = VisionCfg(classes=[0, 2])
    nav: NavCfg = NavCfg(
        waypoints=[
            [10, 10, -10],
            [10, 12, -20.81],
            [15, 60, -4],
            [22, 29, -13.88]
        ]
    )
    recording: RecordingCfg = RecordingCfg()



def load_config() -> Config:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/default.yaml")
    args, _ = parser.parse_known_args()

    with open(args.config, "r") as f:
        y = yaml.safe_load(f)

    def merge(dataclass_type, values):
        obj = dataclass_type()
        for k, v in values.items():
            setattr(obj, k, v)
        return obj

    return Config(
        airsim=merge(AirSimCfg, y.get("airsim", {})),
        vision=merge(VisionCfg, y.get("vision", {})),
        nav=merge(NavCfg, y.get("nav", {})),
        recording=merge(RecordingCfg, y.get("recording", {})),

    )
