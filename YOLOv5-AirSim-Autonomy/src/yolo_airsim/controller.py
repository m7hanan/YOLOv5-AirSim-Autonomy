import time
from yolo_airsim.utils.airsim_helpers import AirSimDrone


class DroneController:
    """
    High-level drone controller that integrates YOLO detections with AirSim.
    """

    def __init__(self, detector, step_delay=0.2):
        self.drone = AirSimDrone()
        self.detector = detector
        self.step_delay = step_delay

    def run_mission(self, waypoints: list, conf_thres: float = 0.3):
        """
        Fly drone through waypoints, detect objects at each step.

        Args:
            waypoints (list): list of (x, y, z) positions.
            conf_thres (float): confidence threshold for detection.
        """
        self.drone.takeoff()

        for wp in waypoints:
            print(f"[INFO] Flying to {wp} ...")
            self.drone.fly_to(wp)
            time.sleep(self.step_delay)

            # Capture frame
            frame = self.drone.capture_frame()

            # Run detection
            detections = self.detector.detect(frame, conf_thres=conf_thres)

            # Log detections
            if detections:
                print(f"[DETECTED] {len(detections)} objects")
                for d in detections:
                    print(f" - {d['label']} ({d['conf']:.2f}) @ {d['bbox']}")
            else:
                print("[INFO] No objects detected.")

        self.drone.land()