class JPiece:

    def __init__(self, image, x_pos, y_pos):
        self.image = image
        self.x_pos = x_pos
        self.y_pos = y_pos


class JGrid:
    def __init__(self, image, n_rows, n_cols):
        self.n_rows = n_rows
        self.n_cols = n_cols
        self.image = image

    def template_match(v):
        print()


class Jigsaw:

    def __init__(self, image, n_rows, n_cols, height_cm, width_cm):
        self.grid = JGrid(image, n_cols, n_rows)
        self.height_cm: int = height_cm
        self.width_cm: int = width_cm
