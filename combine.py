import tkinter as tk
import numpy as np

# Define individual game classes
class DotsAndBoxes:
    # Your Dots and Boxes implementation
    import tkinter as tk
    import numpy as np

# Constants
SIZE_OF_BOARD = 600
NUMBER_OF_DOTS = 6
SYMBOL_SIZE = (SIZE_OF_BOARD / 3 - SIZE_OF_BOARD / 8) / 2
SYMBOL_THICKNESS = 50
DOT_COLOR = '#000000'
PLAYER1_COLOR = '#0492CF'
PLAYER1_COLOR_LIGHT = '#67B0CF'
PLAYER2_COLOR = '#EE4035'
PLAYER2_COLOR_LIGHT = '#EE7E77'
GREEN_COLOR = '#7BC043'
DOT_WIDTH = 0.25 * SIZE_OF_BOARD / NUMBER_OF_DOTS
EDGE_WIDTH = 0.1 * SIZE_OF_BOARD / NUMBER_OF_DOTS
DISTANCE_BETWEEN_DOTS = SIZE_OF_BOARD / NUMBER_OF_DOTS

class DotsAndBoxes:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Dots and Boxes")
        self.canvas = tk.Canvas(self.window, width=SIZE_OF_BOARD, height=SIZE_OF_BOARD)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)
        
        self.player1_starts = True
        self.reset_game()

    def reset_game(self):
        self.board_status = np.zeros((NUMBER_OF_DOTS - 1, NUMBER_OF_DOTS - 1))
        self.row_status = np.zeros((NUMBER_OF_DOTS, NUMBER_OF_DOTS - 1))
        self.col_status = np.zeros((NUMBER_OF_DOTS - 1, NUMBER_OF_DOTS))
        
        self.player1_turn = not self.player1_starts
        self.reset_board = False
        self.already_marked_boxes = []
        self.turntext_handle = None
        
        self.refresh_board()
        self.display_turn_text()

    def mainloop(self):
        self.window.mainloop()

    def is_grid_occupied(self, logical_position, edge_type):
        r, c = logical_position
        if edge_type == 'row':
            return self.row_status[c][r] == 1
        elif edge_type == 'col':
            return self.col_status[c][r] == 1
        return False

    def convert_grid_to_logical_position(self, grid_position):
        position = (np.array(grid_position) - DISTANCE_BETWEEN_DOTS / 4) // (DISTANCE_BETWEEN_DOTS / 2)

        if position[1] % 2 == 0 and (position[0] - 1) % 2 == 0:
            return [int((position[0] - 1) // 2), int(position[1] // 2)], 'row'
        elif position[0] % 2 == 0 and (position[1] - 1) % 2 == 0:
            return [int(position[0] // 2), int((position[1] - 1) // 2)], 'col'
        return None, None

    def update_board(self, edge_type, logical_position):
        r, c = logical_position
        val = -1 if self.player1_turn else 1

        if c < NUMBER_OF_DOTS - 1 and r < NUMBER_OF_DOTS - 1:
            self.board_status[c][r] += val

        if edge_type == 'row':
            self.row_status[c][r] = 1
            if c > 0:
                self.board_status[c - 1][r] += val
        elif edge_type == 'col':
            self.col_status[c][r] = 1
            if r > 0:
                self.board_status[c][r - 1] += val

    def is_gameover(self):
        return np.all(self.row_status == 1) and np.all(self.col_status == 1)

    def make_edge(self, edge_type, logical_position):
        r, c = logical_position
        color = PLAYER1_COLOR if self.player1_turn else PLAYER2_COLOR

        if edge_type == 'row':
            start_x = DISTANCE_BETWEEN_DOTS / 2 + r * DISTANCE_BETWEEN_DOTS
            end_x = start_x + DISTANCE_BETWEEN_DOTS
            start_y = end_y = DISTANCE_BETWEEN_DOTS / 2 + c * DISTANCE_BETWEEN_DOTS
        else:
            start_y = DISTANCE_BETWEEN_DOTS / 2 + c * DISTANCE_BETWEEN_DOTS
            end_y = start_y + DISTANCE_BETWEEN_DOTS
            start_x = end_x = DISTANCE_BETWEEN_DOTS / 2 + r * DISTANCE_BETWEEN_DOTS

        self.canvas.create_line(start_x, start_y, end_x, end_y, fill=color, width=EDGE_WIDTH)

    def mark_box(self):
        for box, color in zip([-4, 4], [PLAYER1_COLOR_LIGHT, PLAYER2_COLOR_LIGHT]):
            for pos in np.argwhere(self.board_status == box):
                if list(pos) not in self.already_marked_boxes:
                    self.already_marked_boxes.append(list(pos))
                    self.shade_box(pos, color)

    def shade_box(self, box, color):
        start_x = DISTANCE_BETWEEN_DOTS / 2 + box[1] * DISTANCE_BETWEEN_DOTS + EDGE_WIDTH / 2
        start_y = DISTANCE_BETWEEN_DOTS / 2 + box[0] * DISTANCE_BETWEEN_DOTS + EDGE_WIDTH / 2
        end_x = start_x + DISTANCE_BETWEEN_DOTS - EDGE_WIDTH
        end_y = start_y + DISTANCE_BETWEEN_DOTS - EDGE_WIDTH
        self.canvas.create_rectangle(start_x, start_y, end_x, end_y, fill=color, outline="")

    def refresh_board(self):
        self.canvas.delete("all")
        for i in range(NUMBER_OF_DOTS):
            pos = DISTANCE_BETWEEN_DOTS / 2 + i * DISTANCE_BETWEEN_DOTS
            self.canvas.create_line(pos, DISTANCE_BETWEEN_DOTS / 2, pos, SIZE_OF_BOARD - DISTANCE_BETWEEN_DOTS / 2, fill="gray", dash=(2, 2))
            self.canvas.create_line(DISTANCE_BETWEEN_DOTS / 2, pos, SIZE_OF_BOARD - DISTANCE_BETWEEN_DOTS / 2, pos, fill="gray", dash=(2, 2))

        for i in range(NUMBER_OF_DOTS):
            for j in range(NUMBER_OF_DOTS):
                x = i * DISTANCE_BETWEEN_DOTS + DISTANCE_BETWEEN_DOTS / 2
                y = j * DISTANCE_BETWEEN_DOTS + DISTANCE_BETWEEN_DOTS / 2
                self.canvas.create_oval(x - DOT_WIDTH / 2, y - DOT_WIDTH / 2, x + DOT_WIDTH / 2, y + DOT_WIDTH / 2, fill=DOT_COLOR, outline=DOT_COLOR)

    def display_turn_text(self):
        text = f"Next turn: {'Player 1' if self.player1_turn else 'Player 2'}"
        color = PLAYER1_COLOR if self.player1_turn else PLAYER2_COLOR

        if self.turntext_handle:
            self.canvas.delete(self.turntext_handle)
        self.turntext_handle = self.canvas.create_text(SIZE_OF_BOARD - 5 * len(text), SIZE_OF_BOARD - DISTANCE_BETWEEN_DOTS / 8, font="cmr 15 bold", text=text, fill=color)

    def display_gameover(self):
        player1_score = np.sum(self.board_status == -4)
        player2_score = np.sum(self.board_status == 4)

        if player1_score > player2_score:
            text, color = "Winner: Player 1", PLAYER1_COLOR
        elif player2_score > player1_score:
            text, color = "Winner: Player 2", PLAYER2_COLOR
        else:
            text, color = "It's a tie", "gray"

        self.canvas.delete("all")
        self.canvas.create_text(SIZE_OF_BOARD / 2, SIZE_OF_BOARD / 3, font="cmr 50 bold", fill=color, text=text)
        score_text = f"Scores\nPlayer 1: {player1_score}\nPlayer 2: {player2_score}"
        self.canvas.create_text(SIZE_OF_BOARD / 2, SIZE_OF_BOARD / 2, font="cmr 30 bold", fill=GREEN_COLOR, text=score_text)
        self.reset_board = True

    def click(self, event):
        if self.reset_board:
            self.reset_game()
            return

        grid_position = [event.x, event.y]
        logical_position, edge_type = self.convert_grid_to_logical_position(grid_position)

        if edge_type and not self.is_grid_occupied(logical_position, edge_type):
            self.update_board(edge_type, logical_position)
            self.make_edge(edge_type, logical_position)
            self.mark_box()

            if self.is_gameover():
                self.display_gameover()
            else:
                self.player1_turn = not self.player1_turn
                self.display_turn_text()



    pass

class HangmanGame:
    # Your Hangman implementation
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



    pass

class TicTacToeGame:
    # Your Tic Tac Toe implementation
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



    pass

class MemoryMatchGame:
    # Your Memory Match implementation
    import tkinter as tk
import random
import time


class MemoryMatchGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Memory Match Game")
        self.card_size = 200
        self.grid_size = 3  # 6x6 grid
        self.canvas_width = self.grid_size * self.card_size + 20
        self.canvas_height = self.grid_size * self.card_size + 20

        self.canvas = tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        self.cards = []
        self.first_card = None
        self.second_card = None
        self.matches = 0
        self.images = []
        self.revealed = set()
        self.start_time = 0
        self.timer_label = None
        self.all_time_best = float("inf")  # Initialize all-time best time

        self.create_start_screen()
        self.window.mainloop()

    def create_start_screen(self):
        self.canvas.delete("all")
        self.revealed.clear()

        self.canvas.create_text(
            self.canvas_width // 2, self.canvas_height // 4, text="Memory Match Game", font=("Arial", 24)
        )
        self.canvas.create_text(
            self.canvas_width // 2, self.canvas_height // 4 + 50, text="Click Start to Play", font=("Arial", 18)
        )

        if self.all_time_best < float("inf"):
            self.canvas.create_text(
                self.canvas_width // 2,
                self.canvas_height // 4 + 100,
                text=f"All-Time Best: {self.all_time_best:.2f}s",
                font=("Arial", 16),
            )

        self.start_button = self.create_button(
            self.canvas_width // 2 - 50,
            self.canvas_height // 2 - 25,
            self.canvas_width // 2 + 50,
            self.canvas_height // 2 + 25,
            "Start",
            "yellow",
        )
        self.canvas.bind("<Button-1>", self.on_start_screen_click)

    def create_button(self, x1, y1, x2, y2, text, color):
        rect = self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
        self.canvas.create_text((x1 + x2) // 2, (y1 + y2) // 2, text=text, font=("Arial", 16))
        return rect

    def on_start_screen_click(self, event):
        x, y = event.x, event.y
        if self.canvas.find_closest(x, y)[0] == self.start_button:
            self.start_game()

    def start_game(self):
        self.canvas.delete("all")
        self.matches = 0
        self.revealed.clear()

        # Initialize timer
        self.start_time = time.time()
        self.timer_label = tk.Label(self.window, text="Time: 0.00s", font=("Arial", 14))
        self.timer_label.pack()
        self.update_timer()

        self.images = list(range(1, (self.grid_size ** 2 // 2) + 1)) * 2
        random.shuffle(self.images)
        self.cards = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1, y1 = j * self.card_size + 10, i * self.card_size + 10
                x2, y2 = x1 + self.card_size, y1 + self.card_size
                card = self.canvas.create_rectangle(x1, y1, x2, y2, fill="gray", outline="black")
                self.cards[i][j] = card
                self.canvas.tag_bind(card, "<Button-1>", lambda e, row=i, col=j: self.on_card_click(row, col))

    def update_timer(self):
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {elapsed_time:.2f}s")
        if self.matches < self.grid_size ** 2 // 2:
            self.window.after(100, self.update_timer)

    def on_card_click(self, row, col):
        if (row, col) in self.revealed:
            return  # Ignore clicks on revealed cards

        if self.first_card and self.second_card:
            return

        card = self.cards[row][col]
        index = row * self.grid_size + col
        self.canvas.itemconfig(card, fill="white")
        text = self.canvas.create_text(
            (col * self.card_size + 50, row * self.card_size + 50), text=str(self.images[index]), font=("Arial", 16)
        )

        if not self.first_card:
            self.first_card = (row, col, text)
        else:
            self.second_card = (row, col, text)
            self.window.after(500, self.check_match)

    def check_match(self):
        row1, col1, text1 = self.first_card
        row2, col2, text2 = self.second_card
        index1 = row1 * self.grid_size + col1
        index2 = row2 * self.grid_size + col2

        if self.images[index1] == self.images[index2]:
            self.matches += 1
            self.revealed.add((row1, col1))
            self.revealed.add((row2, col2))

            if self.matches == self.grid_size ** 2 // 2:
                self.end_game()
        else:
            self.canvas.itemconfig(self.cards[row1][col1], fill="gray")
            self.canvas.itemconfig(self.cards[row2][col2], fill="gray")
            self.canvas.delete(text1)
            self.canvas.delete(text2)

        self.first_card = None
        self.second_card = None

    def end_game(self):
        elapsed_time = time.time() - self.start_time
        self.timer_label.config(text=f"Time: {elapsed_time:.2f}s")

        if elapsed_time < self.all_time_best:
            self.all_time_best = elapsed_time

        self.canvas.create_text(
            self.canvas_width // 2, self.canvas_height // 2 - 50, text="You Win!", font=("Arial", 32)
        )
        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height // 2,
            text=f"Your Time: {elapsed_time:.2f}s\nAll-Time Best: {self.all_time_best:.2f}s",
            font=("Arial", 16),
        )

        # Add "Play Again" button
        self.play_again_button = self.create_button(
            self.canvas_width // 2 - 75,
            self.canvas_height - 100,
            self.canvas_width // 2 + 75,
            self.canvas_height - 50,
            "Restart",
            "lightblue",
        )
        self.canvas.bind("<Button-1>", self.on_play_again_click)

        # Auto-restart after 5 seconds
        self.window.after(5000, self.create_start_screen)

    def on_play_again_click(self, event):
        x, y = event.x, event.y
        if self.canvas.find_closest(x, y)[0] == self.play_again_button:
            self.create_start_screen()


    pass

# Main Menu Function
def main_menu():
    def launch_game(game_class):
        main_window.destroy()
        game = game_class()
        game.mainloop()

    main_window = tk.Tk()
    main_window.title("Game Hub")
    tk.Label(main_window, text="Welcome to the Game Hub!", font=("Helvetica", 16)).pack(pady=20)

    # Buttons for each game
    tk.Button(main_window, text="Dots and Boxes", command=lambda: launch_game(DotsAndBoxes)).pack(pady=10)
    tk.Button(main_window, text="Hangman", command=lambda: launch_game(HangmanGame)).pack(pady=10)
    tk.Button(main_window, text="Tic Tac Toe", command=lambda: launch_game(TicTacToeGame)).pack(pady=10)
    tk.Button(main_window, text="Memory Match", command=lambda: launch_game(MemoryMatchGame)).pack(pady=10)
    tk.Button(main_window, text="Exit", command=main_window.destroy).pack(pady=20)

    main_window.mainloop()

# Main entry point
if __name__ == "__main__":
    main_menu()
