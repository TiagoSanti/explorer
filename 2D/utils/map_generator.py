import os
import random
import numpy as np


def generate_maze(width, height):
    print(f"Starting maze generation for {width}x{height} map")
    maze = np.ones((height, width), dtype=int)  # Initialize maze with walls (1)

    # Define the directions (down, up, right, left)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    def is_valid(x, y):
        # Check if (x, y) is within the maze bounds and is a wall
        return 0 <= x < width and 0 <= y < height and maze[y, x] == 1

    def carve_passage(x, y):
        maze[y, x] = 0  # Mark the current cell as part of the maze
        random.shuffle(directions)  # Shuffle the directions for random carving

        for dx, dy in directions:
            nx, ny = x + 2 * dx, y + 2 * dy  # Step two cells away

            if is_valid(nx, ny):  # If the next cell is valid and unvisited
                maze[y + dy, x + dx] = 0  # Carve through the wall to the next cell
                carve_passage(nx, ny)  # Recursively carve from the new cell

    # Start carving from a random position
    start_x, start_y = random.randrange(1, width, 2), random.randrange(1, height, 2)
    print(f"Starting position for maze carving: ({start_x}, {start_y})")
    carve_passage(start_x, start_y)

    print("Maze generation completed")
    return maze


def format_maze_to_env(maze):
    print("Formatting maze to environment format")
    height, width = maze.shape
    env = np.full((height + 2, width + 2), -1, dtype=int)  # Add borders
    env[1:-1, 1:-1] = maze * (
        -1
    )  # Invert maze: 1 (wall) -> -1 (obstacle), 0 (path) -> 0 (unexplored)

    # Randomly place the player start position (value 2)
    free_cells = np.argwhere(env[1:-1, 1:-1] == 0)
    start_y, start_x = random.choice(free_cells)
    env[start_y + 1, start_x + 1] = 2  # Adjust indices due to borders
    print(f"Player start position set at: ({start_x+1}, {start_y+1})")

    return env


def adjust_obstacle_density(env, desired_density):
    print(f"Adjusting obstacle density to {desired_density:.2f}")
    # Calculate the current density of obstacles
    height, width = env.shape
    total_cells = (height - 2) * (width - 2)  # Exclude borders
    current_obstacles = np.sum(env[1:-1, 1:-1] == -1)
    current_density = current_obstacles / total_cells
    print(f"Current obstacle density: {current_density:.2f}")

    # Determine the number of additional obstacles needed
    desired_obstacles = int(desired_density * total_cells)
    print(f"Desired obstacle count: {desired_obstacles}")
    additional_obstacles = desired_obstacles - current_obstacles
    print(f"Additional obstacles needed: {additional_obstacles}")

    if additional_obstacles > 0:
        # Randomly select free cells and convert them to obstacles
        free_cells = list(zip(*np.where(env[1:-1, 1:-1] == 0)))
        random.shuffle(free_cells)
        for y, x in free_cells[:additional_obstacles]:
            # check if the cell will be surrounded by obstacles
            if np.sum(env[y : y + 3, x : x + 3] == -1) < 8:
                env[y + 1, x + 1] = -1  # Adjust for border

    if additional_obstacles < 0:
        # Randomly select obstacle cells and convert them to free cells
        obstacle_cells = list(zip(*np.where(env[1:-1, 1:-1] == -1)))
        random.shuffle(obstacle_cells)
        for y, x in obstacle_cells[:-additional_obstacles]:
            env[y + 1, x + 1] = 0

    print("Obstacle density adjustment completed")
    return env


def save_map_to_file(map_array, file_path):
    print(f"Saving map to file: {file_path}")
    with open(file_path, "w") as f:
        for row in map_array:
            f.write(" ".join(map(str, row)) + "\n")
    print(f"Map saved successfully: {file_path}")


def generate_n_maps(n, width, height, obstacle_density, maps_dir="maps"):
    print(
        f"Starting generation of {n} maps with size {width}x{height} and OD={obstacle_density:.2f}"
    )
    if not os.path.exists(maps_dir):
        os.makedirs(maps_dir)

    maps_count = len(os.listdir(maps_dir))

    for i in range(n):
        print(f"Generating map {maps_count+(i+1)}...")

        # Generate the maze
        maze = generate_maze(width, height)

        # Convert maze to environment format
        env = format_maze_to_env(maze)

        # Adjust obstacle density
        env = adjust_obstacle_density(env, obstacle_density)

        # Save the map to a file
        file_path = os.path.join(
            maps_dir,
            f"map_h{height}_w{width}_od{str(obstacle_density).replace('.', '')}_{maps_count+i+1:03d}.txt",
        )
        save_map_to_file(env, file_path)
        print(f"Map {maps_count+(i+1)} generated and saved successfully")

    print("Map generation process completed")


if __name__ == "__main__":
    n = 1  # Number of maps to generate
    width = 10  # Width of each map (must be odd for maze generation)
    height = 10  # Height of each map (must be odd for maze generation)
    obstacle_density = 0.35  # Desired obstacle density

    generate_n_maps(n, width, height, obstacle_density)
