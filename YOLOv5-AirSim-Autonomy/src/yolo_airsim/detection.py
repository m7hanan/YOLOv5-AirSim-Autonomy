import cv2
import torch
import numpy as np
from pathlib import Path
from yolo_airsim.utils.vision import preprocess_image, draw_detections


class YOLODetector:
    """
    Wrapper around a YOLO model for object detection in AirSim.
    """

    def __init__(self, weights: str = "yolov5s.pt", device: str = "cuda"):
        self.device = torch.device(device if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load("ultralytics/yolov5", "custom", path=weights)
        self.model.to(self.device).eval()

    def detect(self, frame: np.ndarray, conf_thres: float = 0.3):
        """
        Run YOLO detection on a frame.

        Args:
            frame (np.ndarray): BGR image from AirSim.
            conf_thres (float): confidence threshold.

        Returns:
            results (list[dict]): list of detections with {label, conf, bbox}.
        """
        # Preprocess
        img = preprocess_image(frame)

        # Inference
        results = self.model(img, size=640)
        detections = results.pandas().xyxy[0]  # DataFrame

        output = []
        for _, row in detections.iterrows():
            if row["confidence"] < conf_thres:
                continue
            output.append(
                {
                    "label": row["name"],
                    "conf": float(row["confidence"]),
                    "bbox": [
                        int(row["xmin"]),
                        int(row["ymin"]),
                        int(row["xmax"]),
                        int(row["ymax"]),
                    ],
                }
            )

        return output

    def annotate(self, frame: np.ndarray, detections: list):
        """
        Draw bounding boxes + labels on the frame.

        Args:
            frame (np.ndarray): BGR image.
            detections (list): list of detection dicts.

        Returns:
            frame (np.ndarray): annotated image.
        """
        return draw_detections(frame, detections)