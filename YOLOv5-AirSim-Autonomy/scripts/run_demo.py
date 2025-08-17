from yolo_airsim.config import load_config
from yolo_airsim.controller import AirSimDroneController


def main():
    cfg = load_config()
    drone = AirSimDroneController(cfg)
    try:
        drone.takeoff()
        for wp in cfg.nav.waypoints:
            drone.fly_to_waypoint(*wp, speed=cfg.nav.speed)
        drone.slow_land()
    finally:
        drone.shutdown()


if __name__ == "__main__":
    main()