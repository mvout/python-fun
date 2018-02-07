"""
A simple TicTacToe game.

Welcome to play Tic-Tac-Toe! The game is a classic variation and
the rules are as follows:
 - 2 players
 - X for player 1, O for player 2
 - Game field is 3x3
 - Players put their mark on the game field once per turn
 - Mark can only be based on an empty cell
 - First player to put 3 marks of their own in a single row,
   column or diagonal is the winner
 - If no winner is found before the game field is full the game is
   a draw

The game tracks wins. It is also possible to reset the tracking.

Game checks that the player move is legal. Player is requested to
try again if the move is illegal.

All game related information is printed at the bottom of the window.

It is possible to change the look of the game by choosing one
of the predefined themes.

"""

from tkinter import *

# GLOBAL VARIABLES
PLAYER_NUMBER = 2
FIELD_SIZE = 3  # Can be changed to play on a bigger field
PICTURES = ["empty.gif", "x.gif", "o.gif"]
THEME_LIST = {
    "Light": {
        "bg": "white",
        "buttons": "light grey",
        "fg": "black"
    },
    "Dark": {
        "bg": "black",
        "buttons": "red",
        "fg": "white"
    },
    "Colourful": {
        "bg": "red",
        "buttons": "yellow",
        "fg": "black"
    }
}


class TicTacToe:
    """
    Define a new tic-tac-toe game class
    """

    def __init__(self):

        # Create frames
        self.__window = Tk()
        self.__point_frame = Frame(self.__window, bd=0)
        self.__point_frame.grid(row=0, column=0)
        self.__button_frame = Frame(self.__window, bd=0)
        self.__button_frame.grid(row=2, column=0)
        self.__game_frame = Frame(self.__window, bd=0)
        self.__game_frame.grid(row=1, column=3)
        self.__info_frame = Frame(self.__window, bd=0)
        self.__info_frame.grid(row=2, column=3)

        self.__window.title("Tic-Tac-Toe")
        self.__turn = 0
        self.__turn_number = 0
        self.__player_points = [0] * PLAYER_NUMBER
        self.__board = [[0] * FIELD_SIZE for i in range(FIELD_SIZE)]
        self.__infolabel = Label(self.__info_frame, bd=0)
        self.__infotext = ""
        self.__result_text = ""
        self.__keep_theme = "Light"
        self.__infolabel.grid(row=FIELD_SIZE + 3, column=0, rowspan=3)

        # Dropdown
        self.__theme = StringVar(self.__window)
        self.__theme.set("Light")
        self.__dropdown = OptionMenu(self.__button_frame, self.__theme, *THEME_LIST)
        self.__dropdown.grid(column=0, row=4)

        # Game field pictures
        self.__picture_list = []
        for pic in PICTURES:
            picture = PhotoImage(file=pic)
            self.__picture_list.append(picture)

        # Game field buttons
        self.__field_labels = []
        for r in range(FIELD_SIZE):
            new_list = []
            for c in range(FIELD_SIZE):
                new_cell = Button(self.__game_frame, command=lambda i=r, j=c: \
                    self.boardstate(i, j), highlightbackground="black")
                new_cell.grid(column=c + 2, row=r + 1)
                new_list.append(new_cell)
            self.__field_labels.append(new_list)

        # Players
        self.__player_labels = []
        for i in range(PLAYER_NUMBER):
            new_player_label = Label(self.__point_frame,
                                     text="Player %d wins: " % (i + 1), bd=0)
            new_player_label.grid(row=i, column=0)
            self.__player_labels.append(new_player_label)

        # Win counts
        self.__winlabels = []
        for i in range(PLAYER_NUMBER):
            new_winlabel = Label(self.__point_frame, bd=0)
            new_winlabel.grid(row=i, column=1)
            self.__winlabels.append(new_winlabel)

        # Buttons
        self.__new_game_button = Button(self.__button_frame, text="New Game",
                                        command=self.initialize_board,
                                        height=1, width=12)
        self.__new_game_button.grid(row=2, column=0)

        self.__reset_button = Button(self.__button_frame, text="Reset",
                                     command=self.reset, height=1, width=12)
        self.__reset_button.grid(row=3, column=0)

        self.initialize_board()

    def initialize_board(self):
        """
        Clears the game field and puts the game ready for the next round
        """

        self.__dropdown.destroy()
        self.__theme = StringVar(self.__window)
        self.__theme.set(self.__keep_theme)
        self.__dropdown = OptionMenu(self.__button_frame, self.__theme, *THEME_LIST)
        self.__dropdown.configure(height=1, width=10,
                                  highlightbackground=THEME_LIST[self.__theme.get()]["bg"])
        self.__dropdown.grid(column=0, row=4)
        self.__theme.trace("w", self.change_theme)

        self.__board = [[0] * FIELD_SIZE for i in range(FIELD_SIZE)]
        for button in self.__field_labels:
            for i in range(len(button)):
                button[i].configure(state="normal", bd=0)
        self.__new_game_button.configure(bg=THEME_LIST[self.__theme.get()]["bg"])
        self.__turn = 0
        self.__turn_number = 1
        self.__infotext = "Player %d's turn." % (self.__turn + 1)
        self.__result_text = ""
        self.__infolabel.configure(text=self.__infotext)
        self.__player1_mark = self.__picture_list[1]
        self.__player2_mark = self.__picture_list[2]
        i = 0
        for label in self.__field_labels:
            for slot in label:
                slot.configure(image=self.__picture_list[0])

        self.update_texts()
        self.change_theme()

    def change_theme(self, *args):
        """
        Change the color scheme of the game.
        :param args: Value from the dropdown
        """

        # Get the dropdown value as string
        theme = self.__theme.get()
        self.__window.configure(bg=THEME_LIST[theme]["bg"])
        self.__game_frame.configure(bg=THEME_LIST[theme]["bg"])
        self.__info_frame.configure(bg=THEME_LIST[theme]["bg"])
        self.__button_frame.configure(bg=THEME_LIST[theme]["bg"])
        self.__point_frame.configure(bg=THEME_LIST[theme]["bg"])
        for player in self.__player_labels:
            player.configure(bg=THEME_LIST[theme]["bg"],
                             fg=THEME_LIST[theme]["fg"])
        self.__new_game_button.configure(bg=THEME_LIST[theme]["buttons"],
                                         fg=THEME_LIST[theme]["fg"],
                                         highlightbackground=THEME_LIST[theme]["bg"])
        self.__reset_button.configure(bg=THEME_LIST[theme]["buttons"],
                                      fg=THEME_LIST[theme]["fg"],
                                      highlightbackground=THEME_LIST[theme]["bg"])
        self.__infolabel.configure(bg=THEME_LIST[theme]["bg"],
                                   fg=THEME_LIST[theme]["fg"])
        for win in self.__winlabels:
            win.configure(bg=THEME_LIST[theme]["bg"], fg=THEME_LIST[theme]["fg"])
        self.__dropdown.configure(bg=THEME_LIST[theme]["buttons"],
                                  fg=THEME_LIST[theme]["fg"],
                                  highlightbackground=THEME_LIST[theme]["bg"])
        # Remember the theme so it's not reseted when "New Game" button
        # is pressed.
        self.__keep_theme = theme

    def reset(self):
        """
        Reset the game fully.
        """

        self.__player_points = [0] * PLAYER_NUMBER
        self.__keep_theme = "Light"
        self.initialize_board()

    def change_mark(self, i, j):
        """
        Change the picture of game field button to correspond the
        mark of the player
        :param i: row
        :param j: col
        """

        if self.__turn == 0:
            self.__field_labels[i][j].configure(image=self.__player1_mark)
        elif self.__turn == 1:
            self.__field_labels[i][j].configure(image=self.__player2_mark)

    def boardstate(self, i, j):
        """
        Check if the player move is legal.
        :param i: row
        :param j: column
        """

        try:
            if self.__turn == 0 and self.__board[i][j] == 0:
                self.__board[i][j] = 2
                self.change_mark(i, j)
            elif self.__turn == 1 and self.__board[i][j] == 0:

                self.__board[i][j] = 2 ** FIELD_SIZE
                self.change_mark(i, j)
            else:
                raise ValueError
            self.win_check()  # Check if move caused a win.
        except ValueError:
            self.__infotext = "Choose an empty slot!\n Please try again"
            self.__infolabel.configure(text=self.__infotext)

    def change_turn(self):
        """
        Changes the turn.
        """

        if self.__turn_number <= FIELD_SIZE ** 2:
            if self.__turn_number % 2 == 0:
                self.__turn = 0
            else:
                self.__turn = 1
            self.__turn_number += 1
            self.update_texts()

    def win_check(self):
        """
        Check if a player won.
        """

        d = False  # Tracks a draw
        # Horizontal win
        for i in range(FIELD_SIZE):
            check = self.check_sum(self.__board[i])
            if check:
                self.end(d)
                return

        # Vertical win
        board_transpose = [[row[i] for row in self.__board] for i in \
                           range(FIELD_SIZE)]

        for i in range(FIELD_SIZE):
            check = self.check_sum(board_transpose[i])
            if check:
                self.end(d)
                return

        # Diagonal win
        # Left to right
        n = 0
        ltr = []
        for i in self.__board:
            ltr.append(i[n])
            n += 1
        check = self.check_sum(ltr)
        if check:
            self.end(d)
            return
        # Right to left
        n = FIELD_SIZE - 1
        rtl = []
        for i in self.__board:
            rtl.append(i[n])
            n -= 1
        check = self.check_sum(rtl)
        if check:
            self.end(d)
            return
        else:
            if self.__turn_number == FIELD_SIZE * FIELD_SIZE:
                self.__result_text = "Draw!"
                d = True
                self.end(d)
            else:
                self.change_turn()

    def check_sum(self, l):
        """
        Check the sums of different win conditions
        :param l: list of values corresponding to boardstate
        :return: True if win happened, False if draw or no win
        """

        if sum(l) == 2 * FIELD_SIZE:
            self.__result_text = "Player 1 wins!"
            return True
        elif sum(l) == (2 ** FIELD_SIZE) * FIELD_SIZE:
            self.__result_text = "Player 2 wins!"
            return True
        elif self.__turn_number == FIELD_SIZE * FIELD_SIZE:
            return False
        else:
            return False

    def end(self, d):
        """
        End the game after win or draw.
        :param d: Whether the game was draw or not
        """

        # Disable the game field
        for button in self.__field_labels:
            for i in range(len(button)):
                button[i].configure(state="disabled")

        # Add points if the game was not draw
        if not d:
            self.__player_points[self.__turn] += 1

        self.__infolabel.configure(text=self.__result_text)
        for i in range(len(self.__winlabels)):
            self.__winlabels[i].configure(text=self.__player_points[i])
        self.__new_game_button.configure(bg="green")

    def update_texts(self):
        """
        Update win count and info text.
        """

        for i in range(len(self.__winlabels)):
            self.__winlabels[i].configure(text=self.__player_points[i])
        self.__infotext = "Player %d's turn." % (self.__turn + 1)
        self.__infolabel.configure(text=self.__infotext)

    def start(self):
        """
        Start the game
        """

        self.__window.mainloop()


def main():
    play = TicTacToe()
    play.start()


main()