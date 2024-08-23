import tkinter as tk
from tkinter import filedialog, messagebox
from environment import Environment
from player import Player


class GameGUI:
    def __init__(self, root, environment: Environment, player: Player):
        self.root = root
        self.env = environment
        self.player = player

        self.root.title("2D Exploration Game")
        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack()

        self.cell_size = 50  # Size of each cell in the grid
        self.draw_grid()

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

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.env.height):
            for x in range(self.env.width):
                x1 = x * self.cell_size
                y1 = y * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                if self.env.grid[y, x] == -1:
                    color = "black"  # Obstacles
                elif self.env.grid[y, x] == 0:
                    color = "white"  # Unexplored
                elif self.env.grid[y, x] == 1:
                    color = "gray"  # Explored
                elif self.env.grid[y, x] == 2:
                    color = "blue"  # Player
                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="black"
                )

    def move_player(self, dx, dy):
        self.player.move(dx, dy)
        self.draw_grid()
        if self.env.is_map_complete():
            self.show_completion_message()

    def show_completion_message(self):
        messagebox.showinfo(
            "Game Over", f"Map complete in {len(self.player.moves_list)} moves."
        )
        self.root.quit()
