import io

import torch
from chalice import Chalice
from timm import create_model

from chitra.serve.cloud import ChaliceServer

# MODEL_PATH = "https://github.com/rwightman/pytorch-image-models/releases/download/v0.1-weights/efficientnet_b0_ra-3dd342df.pth"
MODEL_PATH = "examples/assets/model.pth"
url = (
    "https://raw.githubusercontent.com/aniketmaurya/chitra/master/docs/assets/logo.png"
)


def model_loader(buffer: io.BytesIO) -> torch.nn.Module:
    model: torch.nn.Module = create_model("efficientnet_b0", pretrained=False).eval()
    model.load_state_dict(torch.load(buffer))
    return model


def test_cloudserver():
    server = ChaliceServer(
        "image-classification",
        model_path=MODEL_PATH,
        model_loader=model_loader,
    )
    assert isinstance(server.app, Chalice)
    assert isinstance(server.model, torch.nn.Module)


def test_index():
    assert ChaliceServer.index() == {"hello": "world"}


def test_predict():
    class Dummy:
        raw = url

    server = ChaliceServer(
        "image-classification",
        model_path=MODEL_PATH,
        model_loader=model_loader,
    )
    server.app.current_request = Dummy
    assert isinstance(server.predict(), str)
