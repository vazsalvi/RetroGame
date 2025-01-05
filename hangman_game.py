import tkinter as tk
from tkinter import messagebox
import random

class HangmanGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Hangman Game")
        self.window.configure(bg="lightblue")

        self.word_list = ["PYTHON", "HANGMAN", "COMPUTER"]
        self.selected_word = random.choice(self.word_list)
        self.guesses = set()
        self.max_attempts = 6
        self.attempts_left = self.max_attempts

        self.setup_ui()
        self.window.mainloop()

    def setup_ui(self):
        # Title
        tk.Label(
            self.window,
            text="Hangman Game",
            font=("Arial", 24, "bold"),
            bg="lightblue",
            fg="darkblue"
        ).pack(pady=10)

        # Word display
        self.word_display = tk.Label(
            self.window,
            text=self.get_display_word(),
            font=("Arial", 20, "bold"),
            bg="white",
            fg="black",
            width=20,
            relief="sunken"
        )
        self.word_display.pack(pady=10)

        # Hangman canvas
        self.canvas = tk.Canvas(self.window, width=300, height=300, bg="lightblue", highlightthickness=0)
        self.canvas.pack(pady=10)
        self.draw_hangman()

        # Letter buttons
        self.buttons_frame = tk.Frame(self.window, bg="lightblue")
        self.buttons_frame.pack(pady=10)
        self.create_letter_buttons()

        # Restart button
        self.restart_button = tk.Button(
            self.window,
            text="Restart",
            command=self.restart_game,
            font=("Arial", 14, "bold"),
            bg="orange",
            fg="white",
        )
        self.restart_button.pack(pady=20)

    def create_letter_buttons(self):
        for i, letter in enumerate("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
            btn = tk.Button(
                self.buttons_frame,
                text=letter,
                font=("Arial", 12, "bold"),
                width=4,
                bg="lightgray",
                fg="black",
                command=lambda l=letter: self.make_guess(l)
            )
            btn.grid(row=i // 9, column=i % 9, padx=5, pady=5)

    def draw_hangman(self):
        self.canvas.delete("all")
        if self.attempts_left <= 5:
            self.canvas.create_oval(100, 50, 150, 100, outline="black", width=2)  # Head
        if self.attempts_left <= 4:
            self.canvas.create_line(125, 100, 125, 180, fill="black", width=2)  # Body
        if self.attempts_left <= 3:
            self.canvas.create_line(125, 120, 100, 150, fill="black", width=2)  # Left Arm
        if self.attempts_left <= 2:
            self.canvas.create_line(125, 120, 150, 150, fill="black", width=2)  # Right Arm
        if self.attempts_left <= 1:
            self.canvas.create_line(125, 180, 100, 220, fill="black", width=2)  # Left Leg
        if self.attempts_left <= 0:
            self.canvas.create_line(125, 180, 150, 220, fill="black", width=2)  # Right Leg

    def get_display_word(self):
        return " ".join([letter if letter in self.guesses else "_" for letter in self.selected_word])

    def make_guess(self, letter):
        if letter in self.guesses:
            messagebox.showinfo("Hangman", f"You already guessed '{letter}'.")
            return

        self.guesses.add(letter)
        if letter in self.selected_word:
            self.word_display.config(text=self.get_display_word())
            if "_" not in self.get_display_word():
                self.end_game(won=True)
        else:
            self.attempts_left -= 1
            self.draw_hangman()
            if self.attempts_left == 0:
                self.end_game(won=False)

    def end_game(self, won):
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.DISABLED)

        if won:
            messagebox.showinfo("Hangman", f"Congratulations! You guessed the word '{self.selected_word}'!")
        else:
            messagebox.showinfo("Hangman", f"Game Over! The word was '{self.selected_word}'.")

    def restart_game(self):
        self.selected_word = random.choice(self.word_list)
        self.guesses = set()
        self.attempts_left = self.max_attempts

        self.word_display.config(text=self.get_display_word())
        self.draw_hangman()
        for widget in self.buttons_frame.winfo_children():
            widget.config(state=tk.NORMAL)

if __name__ == "__main__":
    HangmanGame()
