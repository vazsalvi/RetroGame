import tkinter as tk
from tkinter import messagebox
from hangman_game import HangmanGame
from dots_and_boxes import DotsAndBoxes
from tic_tac_toe import TicTacToeGame
from memory_match import MemoryMatchGame

class GameHubApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Game Hub")
        self.root.geometry("400x400")
        self.root.config(bg="#f0f0f0")

        # Frame for the content
        self.frame = tk.Frame(self.root, bg="#f0f0f0")
        self.frame.pack(padx=20, pady=20)

        # Title Label with a modern font and color
        self.title_label = tk.Label(self.frame, text="Welcome to the Game Hub!", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#4CAF50")
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Buttons with styled backgrounds and hover effects
        self.hangman_button = self.create_game_button("Hangman", self.start_hangman)
        self.dots_and_boxes_button = self.create_game_button("Dots and Boxes", self.start_dots_and_boxes)
        self.tic_tac_toe_button = self.create_game_button("Tic Tac Toe", self.start_tic_tac_toe)
        self.memory_match_button = self.create_game_button("Memory Match", self.start_memory_match)
        self.exit_button = self.create_game_button("Exit", self.exit_app, "#F44336")

        # Arrange buttons in grid
        self.hangman_button.grid(row=1, column=0, pady=8, sticky="ew")
        self.dots_and_boxes_button.grid(row=2, column=0, pady=8, sticky="ew")
        self.tic_tac_toe_button.grid(row=3, column=0, pady=8, sticky="ew")
        self.memory_match_button.grid(row=4, column=0, pady=8, sticky="ew")
        self.exit_button.grid(row=5, column=0, pady=10, sticky="ew")

    def create_game_button(self, text, command, bg_color="#2196F3"):
        """Creates a styled game button."""
        button = tk.Button(self.frame, text=text, width=20, height=2, font=("Arial", 12), command=command,
                           bg=bg_color, fg="white", relief="flat", bd=0)
        button.config(activebackground="#64b5f6", activeforeground="white")
        button.bind("<Enter>", lambda e: button.config(bg="#64b5f6"))
        button.bind("<Leave>", lambda e: button.config(bg=bg_color))
        return button

    def start_hangman(self):
        game = HangmanGame()
        game.start_game()

    def start_dots_and_boxes(self):
        game = DotsAndBoxes()
        game.start_game()

    def start_tic_tac_toe(self):
        game = TicTacToeGame()
        game.start_game()

    def start_memory_match(self):
        game = MemoryMatchGame()
        game.start_game()

    def exit_app(self):
        response = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if response:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = GameHubApp(root)
    root.mainloop()
