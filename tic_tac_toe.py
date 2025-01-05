import tkinter as tk
import random

class TicTacToeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Tic-Tac-Toe")

        self.board = [" " for _ in range(9)]  # Initialize a 3x3 board
        self.current_player = "X"  # Player starts first
        self.buttons = []

        self.create_board()
        self.status_label = tk.Label(
            self.window,
            text="Your Turn (X)",
            font=("Arial", 16, "bold"),
            bg="lightgray",
            fg="black",
        )
        self.status_label.grid(row=3, column=0, columnspan=3, pady=10)

        self.restart_button = tk.Button(
            self.window,
            text="Restart",
            command=self.restart_game,
            font=("Arial", 14, "bold"),
            bg="orange",
            fg="white",
            relief="raised",
            bd=3,
        )
        self.restart_button.grid(row=4, column=0, columnspan=3, pady=10)

        self.window.configure(bg="lightblue")
        self.window.mainloop()

    def create_board(self):
        for row in range(3):
            for col in range(3):
                button = tk.Button(
                    self.window,
                    text=" ",
                    font=("Arial", 24, "bold"),
                    width=5,
                    height=2,
                    bg="white",
                    fg="black",
                    relief="ridge",
                    command=lambda r=row, c=col: self.make_move(r, c),
                )
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons.append(button)

    def make_move(self, row, col):
        index = row * 3 + col
        if self.board[index] == " " and self.current_player == "X":
            self.board[index] = "X"
            self.buttons[index].config(text="X", fg="blue", bg="lightyellow", state=tk.DISABLED)
            if self.check_winner("X"):
                self.status_label.config(text="You Win!", fg="green")
                self.disable_board()
            elif " " not in self.board:
                self.status_label.config(text="It's a Tie!", fg="red")
            else:
                self.current_player = "O"
                self.status_label.config(text="Computer's Turn (O)", fg="purple")
                self.window.after(500, self.computer_move)

    def computer_move(self):
        available_moves = [i for i, spot in enumerate(self.board) if spot == " "]
        move = self.best_move(available_moves)
        self.board[move] = "O"
        self.buttons[move].config(text="O", fg="red", bg="lightgray", state=tk.DISABLED)
        if self.check_winner("O"):
            self.status_label.config(text="Computer Wins!", fg="red")
            self.disable_board()
        elif " " not in self.board:
            self.status_label.config(text="It's a Tie!", fg="red")
        else:
            self.current_player = "X"
            self.status_label.config(text="Your Turn (X)", fg="black")

    def best_move(self, available_moves):
        # Try to win or block the player from winning
        for move in available_moves:
            self.board[move] = "O"
            if self.check_winner("O"):
                self.board[move] = " "  # Reset
                return move
            self.board[move] = " "

        for move in available_moves:
            self.board[move] = "X"
            if self.check_winner("X"):
                self.board[move] = " "  # Reset
                return move
            self.board[move] = " "

        # Otherwise, pick a random available move
        return random.choice(available_moves)

    def check_winner(self, player):
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6],             # Diagonals
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                for i in combo:
                    self.buttons[i].config(bg="lightgreen" if player == "X" else "pink")
                return True
        return False

    def disable_board(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)

    def restart_game(self):
        self.board = [" " for _ in range(9)]
        self.current_player = "X"
        for button in self.buttons:
            button.config(text=" ", state=tk.NORMAL, bg="white", fg="black")
        self.status_label.config(text="Your Turn (X)", fg="black")


if __name__ == "__main__":
    TicTacToeGame()
