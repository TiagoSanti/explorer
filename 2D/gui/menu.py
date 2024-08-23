import os
import tkinter as tk
from tkinter import messagebox
import numpy as np
from environment import Environment
from player import Player
from gui.game import GameGUI


class MenuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Exploration Game - Main Menu")

        # Set the window size
        self.root.geometry("400x200")
        self.root.resizable(False, False)

        # Menu title
        self.title_label = tk.Label(
            root, text="2D Exploration Game", font=("Helvetica", 16)
        )
        self.title_label.pack(pady=20)

        # Start Game as Player button
        self.start_game_button = tk.Button(
            root, text="Start Game as Player", command=self.display_maps
        )
        self.start_game_button.pack(pady=10)

        # Exit button
        self.exit_button = tk.Button(root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def display_maps(self):
        # Clear the current menu
        for widget in self.root.winfo_children():
            widget.destroy()

        # Update the window title and size
        self.root.title("Select a Map")
        self.root.geometry("800x400")

        # Create a frame and canvas with a scrollbar
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bind the mouse scroll event
        self.bind_mouse_scroll(canvas)

        # Load maps from the 'maps' folder
        maps_dir = "maps"
        map_files = [f for f in os.listdir(maps_dir) if f.endswith(".txt")]

        if not map_files:
            messagebox.showerror("Error", "No map files found in the 'maps' directory.")
            self.root.quit()
            return

        for i, map_file in enumerate(map_files):
            # Load the map matrix
            matrix_map = self.load_map(os.path.join(maps_dir, map_file))

            if matrix_map is not None:
                # Display the map name
                map_label = tk.Label(scrollable_frame, text=map_file)
                map_label.grid(row=i, column=0, padx=10, pady=5)

                # Create a canvas to draw the miniature
                miniature = self.create_map_miniature(scrollable_frame, matrix_map)
                miniature.grid(row=i, column=1, padx=10, pady=5)

                # Add a button to select this map
                select_button = tk.Button(
                    scrollable_frame,
                    text="Select",
                    command=lambda m=matrix_map: self.start_game(m),
                )
                select_button.grid(row=i, column=2, padx=10, pady=5)

    def bind_mouse_scroll(self, canvas):
        # Bind mouse scroll to the canvas
        canvas.bind_all(
            "<MouseWheel>", lambda event: self._on_mouse_wheel(event, canvas)
        )
        canvas.bind_all("<Button-4>", lambda event: self._on_mouse_wheel(event, canvas))
        canvas.bind_all("<Button-5>", lambda event: self._on_mouse_wheel(event, canvas))

    def _on_mouse_wheel(self, event, canvas):
        if event.num == 4 or event.delta > 0:
            canvas.yview_scroll(-1, "units")
        elif event.num == 5 or event.delta < 0:
            canvas.yview_scroll(1, "units")

    def create_map_miniature(self, parent, matrix_map):
        # Create a small canvas to represent the map
        rows, cols = len(matrix_map), len(matrix_map[0])
        canvas = tk.Canvas(parent, width=cols * 10, height=rows * 10)

        for y, row in enumerate(matrix_map):
            for x, cell in enumerate(row):
                color = self.get_color_for_cell(cell)
                canvas.create_rectangle(
                    x * 10,
                    y * 10,
                    x * 10 + 10,
                    y * 10 + 10,
                    fill=color,
                    outline="black",
                )

        return canvas

    def get_color_for_cell(self, cell_value):
        if cell_value == -1:
            return "black"
        elif cell_value == 0:
            return "white"
        elif cell_value == 1:
            return "gray"
        elif cell_value == 2:
            return "blue"
        return "white"

    def start_game(self, matrix_map):
        # Start the game with the selected map
        self.root.destroy()  # Close the map selection window
        game_root = tk.Tk()
        env = Environment(matrix=matrix_map)
        player = Player(env=env, vision_range=1)
        game_gui = GameGUI(game_root, env, player)
        game_root.mainloop()

    def load_map(self, file_path):
        try:
            with open(file_path, "r") as file:
                lines = file.readlines()
                matrix_map = []
                for line in lines:
                    row = list(map(int, line.strip().split()))
                    matrix_map.append(row)
                return np.array(matrix_map)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load map: {e}")
            return None
