import tkinter as tk
from tkinter import messagebox
from environment import Environment
from player import Player


class GameGUI:
    def __init__(self, root, environment: Environment, player: Player):
        self.root = root
        self.env = environment
        self.player = player

        self.root.title("2D Exploration Game")

        self.padding = 5  # Padding around the grid

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.cell_size = 50  # Default size of each cell in the grid
        self.canvas.bind("<Configure>", self.on_resize)

        # Bind keys for movement
        self.root.bind("<w>", lambda event: self.move_player(0, -1))
        self.root.bind("<s>", lambda event: self.move_player(0, 1))
        self.root.bind("<a>", lambda event: self.move_player(-1, 0))
        self.root.bind("<d>", lambda event: self.move_player(1, 0))

        # Display buttons
        button_frame = tk.Frame(root)
        button_frame.pack()
        tk.Button(
            button_frame, text="Up (w)", command=lambda: self.move_player(0, -1)
        ).grid(row=0, column=1)
        tk.Button(
            button_frame, text="Left (a)", command=lambda: self.move_player(-1, 0)
        ).grid(row=1, column=0)
        tk.Button(
            button_frame, text="Down (s)", command=lambda: self.move_player(0, 1)
        ).grid(row=1, column=1)
        tk.Button(
            button_frame, text="Right (d)", command=lambda: self.move_player(1, 0)
        ).grid(row=1, column=2)

    def on_resize(self, event):
        # Adjust the cell size when the window is resized
        available_width = event.width - 2 * self.padding
        available_height = event.height - 2 * self.padding
        self.cell_size = min(
            available_width // self.env.width, available_height // self.env.height
        )
        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        visible_area = self.player.get_visible_area()

        grid_width = self.env.width * self.cell_size
        grid_height = self.env.height * self.cell_size

        # Calculate top-left corner of the grid to center it
        start_x = (self.canvas.winfo_width() - grid_width) // 2
        start_y = (self.canvas.winfo_height() - grid_height) // 2

        for y in range(self.env.height):
            for x in range(self.env.width):
                x1 = start_x + x * self.cell_size + self.padding
                y1 = start_y + y * self.cell_size + self.padding
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if (x, y) in visible_area:
                    if self.env.grid[y, x] == -1:
                        color = "black"  # Obstacles
                    elif self.env.grid[y, x] == 0:
                        color = "white"  # Unexplored
                    elif self.env.grid[y, x] == 1:
                        color = "gray"  # Explored
                    elif self.env.grid[y, x] == 2:
                        color = "blue"  # Player
                else:
                    color = "darkgray"  # Out of vision range

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="black"
                )

    def move_player(self, dx, dy):
        self.player.move(dx, dy)
        self.draw_grid()
        if self.env.is_map_complete():
            self.show_completion_message()

    def show_completion_message(self):
        self.player.vision_range = self.env.width
        self.draw_grid()
        messagebox.showinfo(
            "Game Over", f"Map completed in {len(self.player.moves_list)} moves."
        )
        self.root.quit()
