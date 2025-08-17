import cv2
import argparse
from yolo_airsim.config import load_config
from yolo_airsim.controller import AirSimDroneController


parser = argparse.ArgumentParser()
parser.add_argument("--output", default="videos/demo.mp4")
parser.add_argument("--fps", type=int, default=30)
args = parser.parse_args()

cfg = load_config()
drone = AirSimDroneController(cfg)
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
writer = None

try:
    drone.takeoff()
    for wp in cfg.nav.waypoints:
        frame = drone.get_airsim_image()
        if frame is None:
            continue
        if writer is None:
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(args.output, fourcc, args.fps, (w, h))
        annotated, _ = drone.detect_objects(frame)
        writer.write(annotated)
        drone.fly_to_waypoint(*wp, speed=cfg.nav.speed)
    drone.slow_land()
finally:
    if writer:
        writer.release()
    drone.shutdown()