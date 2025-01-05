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


if __name__ == "__main__":
    MemoryMatchGame()
