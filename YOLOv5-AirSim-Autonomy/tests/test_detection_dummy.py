import torch
import detection

def test_model_loads():
    model = detection.load_model()
    assert model is not None
