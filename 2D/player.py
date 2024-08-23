from agent import Agent


class Player(Agent):
    def __init__(self, env, vision_range=1):
        super().__init__(env, vision_range)

    def prompt_move(self):
        move_dict = {
            "w": (0, -1),
            "s": (0, 1),
            "a": (-1, 0),
            "d": (1, 0),
        }

        move = input("Move (w/s/a/d or q to quit): ").lower()
        if move == "q":
            print("Quitting...")
            exit()
        if move in move_dict:
            dx, dy = move_dict[move]
            self.move(dx, dy)
        else:
            print("Invalid move")
