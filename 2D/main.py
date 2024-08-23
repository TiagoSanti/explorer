import tkinter as tk
from gui.menu import MenuGUI


def main():
    root = tk.Tk()
    menu_gui = MenuGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
