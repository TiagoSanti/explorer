import numpy as np

DISPLAY_MAP = {
    -1: "X",
    0: ".",
    1: " ",
    2: "A",
}


class Environment:
    def __init__(
        self,
        matrix: np.ndarray = None,
    ):
        if matrix is not None:
            self.grid = matrix
            self.height, self.width = matrix.shape
            self.player_start_y, self.player_start_x = np.argwhere(matrix == 2)[0]
        else:
            raise ValueError("Matrix must be provided")

    def place_borders(self):
        self.grid[0, :] = -1  # Top border
        self.grid[-1, :] = -1  # Bottom border
        self.grid[:, 0] = -1  # Left border
        self.grid[:, -1] = -1  # Right border

    def place_obstacles(self, obstacles):
        for x, y in obstacles:
            self.grid[y, x] = -1

    def update_cell(self, x, y, value):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = value

    def is_map_complete(self) -> bool:
        return not np.any(self.grid == 0)

    def display_grid(self, grid=None):
        if grid is None:
            grid = self.grid

        for row in grid:
            print(" ".join(DISPLAY_MAP[cell] for cell in row))
