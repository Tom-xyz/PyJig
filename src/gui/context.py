from PIL import Image
from dataclasses import dataclass, field, asdict


@dataclass
class AppConfig():
    """
    Mutable app config
    """
    crop_cords: list = field(default_factory=list)
    action: str = None
    orignal_image: Image = None
    viewer_image: Image = None


class WindowContext():

    def __init__(self, window):
        self.window = window
        self.state = asdict(AppConfig())

    def get(self, k):
        return self.state[k]

    def set(self, k, v):
        self.state[k] = v
