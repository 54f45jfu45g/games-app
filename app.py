import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TicTacToeGame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.board = ["" for _ in range(9)]
        self.current_player = "X"
        self.buttons = []

        label = ttk.Label(self.frame, text="Tic-Tac-Toe", font=("Arial", 18, "bold"))
        label.pack(pady=(10, 5))

        self.status = ttk.Label(self.frame, text="Player X's turn", font=("Arial", 12))
        self.status.pack(pady=5)

        board_frame = ttk.Frame(self.frame)
        board_frame.pack(pady=10)

        for i in range(9):
            b = ttk.Button(board_frame, text="", width=6, command=lambda idx=i: self.make_move(idx), style="Game.TButton")
            b.grid(row=i // 3, column=i % 3, padx=5, pady=5)
            self.buttons.append(b)

        reset_btn = ttk.Button(self.frame, text="Reset Game", command=self.reset_game, style="Accent.TButton")
        reset_btn.pack(pady=10)

    def make_move(self, idx):
        if self.board[idx] != "":
            return

        self.board[idx] = self.current_player
        self.buttons[idx].config(text=self.current_player)

        winner = self.check_winner()
        if winner:
            self.status.config(text=f"Player {winner} wins!")
            self.disable_board()
            return

        if all(cell != "" for cell in self.board):
            self.status.config(text="It's a draw!")
            return

        self.current_player = "O" if self.current_player == "X" else "X"
        self.status.config(text=f"Player {self.current_player}'s turn")

    def check_winner(self):
        win_lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for a, b, c in win_lines:
            if self.board[a] and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def disable_board(self):
        for btn in self.buttons:
            btn.config(state="disabled")

    def reset_game(self):
        self.board = ["" for _ in range(9)]
        self.current_player = "X"
        self.status.config(text="Player X's turn")
        for btn in self.buttons:
            btn.config(text="", state="normal")

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


class GuessNumberGame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.secret = random.randint(1, 100)
        self.attempts = 0

        label = ttk.Label(self.frame, text="Guess the Number", font=("Arial", 18, "bold"))
        label.pack(pady=(10, 5))

        instruction = ttk.Label(self.frame, text="Choose a number from 1 to 100", font=("Arial", 11))
        instruction.pack(pady=5)

        entry_frame = ttk.Frame(self.frame)
        entry_frame.pack(pady=10)

        self.entry = ttk.Entry(entry_frame, width=12, font=("Arial", 12))
        self.entry.grid(row=0, column=0, padx=(0, 8))

        self.submit = ttk.Button(entry_frame, text="Guess", command=self.check_guess, style="Accent.TButton")
        self.submit.grid(row=0, column=1)

        self.status = ttk.Label(self.frame, text="Make your first guess!", font=("Arial", 12))
        self.status.pack(pady=10)

        self.history = tk.Listbox(self.frame, width=30, height=8, font=("Arial", 10))
        self.history.pack(pady=(5, 10))

        reset_btn = ttk.Button(self.frame, text="New Game", command=self.reset_game, style="Game.TButton")
        reset_btn.pack()

    def check_guess(self):
        try:
            guess = int(self.entry.get())
        except ValueError:
            self.status.config(text="Please enter a valid number.")
            return

        if guess < 1 or guess > 100:
            self.status.config(text="Number must be between 1 and 100.")
            return

        self.attempts += 1
        self.history.insert(tk.END, f"Attempt {self.attempts}: {guess}")

        if guess == self.secret:
            self.status.config(text=f"Correct! You guessed it in {self.attempts} tries.")
            self.entry.config(state="disabled")
            self.submit.config(state="disabled")
            return

        if guess < self.secret:
            clue = "Too low!"
        else:
            clue = "Too high!"
        self.status.config(text=clue)
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def reset_game(self):
        self.secret = random.randint(1, 100)
        self.attempts = 0
        self.history.delete(0, tk.END)
        self.entry.delete(0, tk.END)
        self.entry.config(state="normal")
        self.submit.config(state="normal")
        self.status.config(text="Make your first guess!")
        self.entry.focus()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


class MemoryGame:
    def __init__(self, parent):
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.symbols = ["🍉", "🍋", "🍇", "🍒", "🍊", "🍎", "🍍", "🥝"]
        self.cards = []
        self.flipped = []
        self.locked = False
        self.matched_pairs = 0

        label = ttk.Label(self.frame, text="Memory Match", font=("Arial", 18, "bold"))
        label.pack(pady=(10, 5))

        self.status = ttk.Label(self.frame, text="Match all pairs!", font=("Arial", 12))
        self.status.pack(pady=5)

        self.grid = ttk.Frame(self.frame)
        self.grid.pack(pady=15)

        self.reset_btn = ttk.Button(self.frame, text="Shuffle Cards", command=self.setup_game, style="Game.TButton")
        self.reset_btn.pack()

        self.setup_game()

    def setup_game(self):
        self.flipped = []
        self.locked = False
        self.matched_pairs = 0
        self.status.config(text="Match all pairs!")

        for child in self.grid.winfo_children():
            child.destroy()

        deck = self.symbols * 2
        random.shuffle(deck)
        self.cards = []

        for i, symbol in enumerate(deck):
            btn = tk.Button(
                self.grid,
                text="?",
                width=6,
                height=3,
                font=("Arial", 18),
                bg="#3b82f6",
                fg="white",
                bd=0,
                activebackground="#60a5fa",
                command=lambda idx=i: self.flip_card(idx)
            )
            btn.grid(row=i // 4, column=i % 4, padx=5, pady=5)
            self.cards.append({"button": btn, "symbol": symbol, "matched": False})

    def flip_card(self, idx):
        if self.locked:
            return

        card = self.cards[idx]
        btn = card["button"]

        if btn.cget("text") != "?" or card["matched"]:
            return

        btn.config(text=card["symbol"], bg="#e2e8f0", fg="black")
        self.flipped.append(idx)

        if len(self.flipped) == 2:
            self.locked = True
            first_idx, second_idx = self.flipped
            first = self.cards[first_idx]
            second = self.cards[second_idx]

            if first["symbol"] == second["symbol"]:
                first["matched"] = True
                second["matched"] = True
                first["button"].config(bg="#22c55e", state="disabled")
                second["button"].config(bg="#22c55e", state="disabled")
                self.matched_pairs += 1
                self.status.config(text=f"Nice! {self.matched_pairs} pairs matched.")
                self.flipped = []
                self.locked = False

                if self.matched_pairs == len(self.symbols):
                    self.status.config(text="You won! All pairs matched!")
            else:
                self.status.config(text="Not a match. Try again!")
                self.parent.after(800, lambda: self.hide_cards(first_idx, second_idx))

    def hide_cards(self, first_idx, second_idx):
        first = self.cards[first_idx]
        second = self.cards[second_idx]
        first["button"].config(text="?", bg="#3b82f6", fg="white")
        second["button"].config(text="?", bg="#3b82f6", fg="white")
        self.flipped = []
        self.locked = False

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()


class GameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GameHub")
        self.root.geometry("720x620")
        self.root.configure(bg="#0f172a")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#0f172a")
        style.configure("TLabel", background="#0f172a", foreground="#f8fafc")
        style.configure("TButton", background="#1f2937", foreground="#ffffff", padding=8)
        style.map("TButton", background=[("active", "#374151")])
        style.configure("Accent.TButton", background="#8b5cf6", foreground="#ffffff", padding=8)
        style.map("Accent.TButton", background=[("active", "#7c3aed")])
        style.configure("Game.TButton", background="#1f2937", foreground="#ffffff", padding=8)
        style.map("Game.TButton", background=[("active", "#334155")])

        top_bar = ttk.Frame(root, padding=20)
        top_bar.pack(fill="x")

        title = ttk.Label(top_bar, text="GameHub", font=("Arial", 24, "bold"))
        title.pack(anchor="w")

        subtitle = ttk.Label(top_bar, text="Play fun mini games", font=("Arial", 11))
        subtitle.pack(anchor="w")

        nav = ttk.Frame(root)
        nav.pack(fill="x", padx=20, pady=(0, 10))

        self.games = {
            "TicTacToe": ttk.Button(nav, text="Tic-Tac-Toe", command=lambda: self.show_game("tic"), style="Game.TButton"),
            "Guess": ttk.Button(nav, text="Guess Number", command=lambda: self.show_game("guess"), style="Game.TButton"),
            "Memory": ttk.Button(nav, text="Memory Match", command=lambda: self.show_game("memory"), style="Game.TButton"),
        }

        for btn in self.games.values():
            btn.pack(side="left", padx=5)

        self.content = ttk.Frame(root)
        self.content.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tic = TicTacToeGame(self.content)
        self.guess = GuessNumberGame(self.content)
        self.memory = MemoryGame(self.content)

        self.show_game("tic")

    def show_game(self, name):
        games = {
            "tic": self.tic,
            "guess": self.guess,
            "memory": self.memory,
        }
        for key, game in games.items():
            if key == name:
                game.show()
            else:
                game.hide()


def main():
    root = tk.Tk()
    app = GameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
