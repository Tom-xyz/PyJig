class WindowContext():

    def __init__(self, window):
        self.window = window
        self.state = {
            'crop_cords': [],
            'action': None,
            'original_image': None,
            'viewer_image': None,
            'puzzle': None
        }

    def get(self, k):
        return self.state[k]

    def set(self, k, v):
        self.state[k] = v
