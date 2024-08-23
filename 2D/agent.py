from environment import Environment


class Agent:
    def __init__(self, env, vision_range=1):
        self.env: Environment = env
        self.x = env.player_start_x
        self.y = env.player_start_y
        self.vision_range = vision_range
        self.env.update_cell(x=self.x, y=self.y, value=2)  # Initial position
        self.moves_list = []

    def move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if self.can_move_to(new_x, new_y):
            self.env.update_cell(x=self.x, y=self.y, value=1)  # Mark as explored
            self.x = new_x
            self.y = new_y
            self.env.update_cell(x=self.x, y=self.y, value=2)  # Update new position
            self.moves_list.append((self.x, self.y))

    def can_move_to(self, x, y):
        return (
            0 <= x < self.env.width
            and 0 <= y < self.env.height
            and self.env.grid[y, x] != -1
        )

    def get_visible_area(self) -> list:
        x_min = max(0, self.x - self.vision_range)
        x_max = min(self.env.width, self.x + self.vision_range + 1)
        y_min = max(0, self.y - self.vision_range)
        y_max = min(self.env.height, self.y + self.vision_range + 1)
        visible_area = [
            (x, y) for x in range(x_min, x_max) for y in range(y_min, y_max)
        ]
        return visible_area
