

import tkinter as tk
import random
import pygame

# Initialize pygame mixer for sound effects
pygame.mixer.init()

# Sound effect files (make sure you have these sound files in the same directory)
MOVE_SOUND = "move_sound.wav"
WIN_SOUND = "win_sound.wav"
TIE_SOUND = "tie_sound.wav"

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("400x600")
        
        # Game state
        self.board = [""] * 9  # 3x3 grid represented as a flat list
        self.current_player = "X"
        self.player_score = 0
        self.computer_score = 0
        self.ties = 0
        self.time_left = 10  # 10 seconds for each turn
        self.is_game_over = False
        
        # UI Elements
        self.buttons = []
        self.create_widgets()
    
    def create_widgets(self):
        """Create the game UI."""
        self.score_label = tk.Label(self.root, text="X: 0 | O: 0", font=("Arial", 14))
        self.score_label.pack(pady=10)
        
        self.result_label = tk.Label(self.root, text="", font=("Arial", 16))
        self.result_label.pack(pady=10)

        # Create game board (buttons)
        frame = tk.Frame(self.root)
        frame.pack()

        for i in range(3):
            for j in range(3):
                button = tk.Button(frame, text="", font=("Arial", 20), width=5, height=2,
                                   command=lambda idx=i*3+j: self.handle_click(idx))
                button.grid(row=i, column=j)
                self.buttons.append(button)
        
        # Restart Button
        restart_button = tk.Button(self.root, text="Restart", font=("Arial", 14), command=self.restart_game)
        restart_button.pack(pady=20)

        # Timer Label
        self.timer_label = tk.Label(self.root, text=f"Time Left: {self.time_left}s", font=("Arial", 14))
        self.timer_label.pack(pady=10)
        
        self.update_score_label()
    
    def play_sound(self, sound_file):
        """Play sound effects."""
        pygame.mixer.Sound(sound_file).play()

    def start_timer(self):
        """Start a countdown timer for each player."""
        self.time_left = 10  # reset to 10 seconds per turn
        self.update_timer()

    def update_timer(self):
        """Update the timer every second."""
        if self.time_left > 0 and not self.is_game_over:
            self.time_left -= 1
            self.timer_label.config(text=f"Time Left: {self.time_left}s")
            self.root.after(1000, self.update_timer)
        else:
            if self.time_left == 0:
                self.switch_player()
    
    def handle_click(self, index):
        """Handle button click event."""
        if self.board[index] == "" and not self.is_game_over:
            self.board[index] = "X"
            self.buttons[index].config(text="X")
            self.animate_button_click(self.buttons[index])
            self.play_sound(MOVE_SOUND)
            if not self.check_winner():
                self.switch_player()
                self.computer_move()
    
    def animate_button_click(self, button):
        """Animate the button click by changing background color briefly."""
        original_color = button.cget("bg")
        button.config(bg="yellow")
        self.root.after(100, lambda: button.config(bg=original_color))

    def switch_player(self):
        """Switch between players."""
        self.current_player = "O" if self.current_player == "X" else "X"
        if self.current_player == "O" and not self.is_game_over:
            self.computer_move()
    
    def minimax(self, board, depth, is_maximizing):
        """Minimax Algorithm for optimal computer move."""
        winner = self.check_winner_in_board(board)
        if winner == "X":
            return -10  # Player wins
        elif winner == "O":
            return 10  # Computer wins
        elif not any(cell == "" for cell in board):
            return 0  # Tie

        if is_maximizing:
            best = -float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "O"
                    best = max(best, self.minimax(board, depth + 1, False))
                    board[i] = ""
            return best
        else:
            best = float('inf')
            for i in range(9):
                if board[i] == "":
                    board[i] = "X"
                    best = min(best, self.minimax(board, depth + 1, True))
                    board[i] = ""
            return best

    def computer_move(self):
        """Improved computer move using Minimax algorithm."""
        available_buttons = [i for i in range(9) if self.board[i] == ""]
        best_move = None
        best_value = -float('inf')

        for move in available_buttons:
            self.board[move] = "O"
            move_value = self.minimax(self.board, 0, False)
            self.board[move] = ""
            if move_value > best_value:
                best_value = move_value
                best_move = move

        if best_move is not None:
            self.board[best_move] = "O"
            self.buttons[best_move].config(text="O")
            self.animate_button_click(self.buttons[best_move])
            self.play_sound(MOVE_SOUND)
            if not self.check_winner():
                self.switch_player()

    def check_winner_in_board(self, board):
        """Check if there is a winner in the current board state."""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combination in winning_combinations:
            if board[combination[0]] == board[combination[1]] == board[combination[2]] and board[combination[0]] != "":
                return board[combination[0]]
        return None
    
    def check_winner(self):
        """Check if there is a winner or a tie."""
        winner = self.check_winner_in_board(self.board)
        if winner:
            self.highlight_winner(winner)
            self.update_score(winner)
            self.show_result(f"{winner} Wins!")
            self.play_sound(WIN_SOUND)
            return True

        if "" not in self.board:  # Check for a tie
            self.highlight_tie()
            self.show_result("Tie! No Winner!")
            self.play_sound(TIE_SOUND)
            self.update_score(None)
            return True

        return False

    def highlight_winner(self, winner):
        """Highlight the winning combination."""
        winning_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        
        for combination in winning_combinations:
            if self.board[combination[0]] == self.board[combination[1]] == self.board[combination[2]] and self.board[combination[0]] != "":
                for idx in combination:
                    self.buttons[idx].config(bg="cyan")

    def highlight_tie(self):
        """Highlight the tie situation."""
        for button in self.buttons:
            button.config(bg="red")

    def show_result(self, message):
        """Display the result of the game."""
        self.result_label.config(text=message, fg="cyan" if "Wins" in message else "red")

    def update_score(self, winner):
        """Update the score and reset the game board."""
        if winner == "X":
            self.player_score += 1
        elif winner == "O":
            self.computer_score += 1
        else:
            self.ties += 1
        
        self.update_score_label()
        self.disable_buttons()

    def update_score_label(self):
        """Update the score label."""
        self.score_label.config(text=f"X: {self.player_score} | O: {self.computer_score}")

    def disable_buttons(self):
        """Disable all the buttons after a game ends."""
        for button in self.buttons:
            button.config(state="disabled")

    def restart_game(self):
        """Restart the game."""
        self.board = [""] * 9
        self.current_player = "X"
        self.is_game_over = False
        for button in self.buttons:
            button.config(text="", bg="SystemButtonFace", state="normal")
        self.result_label.config(text="")
        self.update_score_label()
        self.start_timer()

# Create and run the game
root = tk.Tk()
game = TicTacToe(root)
root.mainloop()
