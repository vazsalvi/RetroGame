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

if __name__ == "__main__":
    game = DotsAndBoxes()
    game.mainloop()
