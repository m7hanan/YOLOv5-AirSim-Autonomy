import cv2
import numpy as np


def preprocess_image(frame: np.ndarray):
    """
    Convert BGR image to RGB and resize for YOLO.
    """
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return img


def draw_detections(frame: np.ndarray, detections: list):
    """
    Draw bounding boxes with labels and confidence on image.
    """
    for det in detections:
        x1, y1, x2, y2 = det["bbox"]
        label = f"{det['label']} {det['conf']:.2f}"

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(
            frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2
        )
    return frame
