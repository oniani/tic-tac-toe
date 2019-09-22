#!/usr/bin/env python3
# encoding: UTF-8

"""
Filename: tic_tac_toe.py
Date: 2019-09-22 04:12:17 PM
Author: David Oniani
E-mail: onianidavid@gmail.com

License:
    The code is licensed under GNU General Public License v3.0.
    Please read the LICENSE file in this distribution for details
    regarding the licensing of this code.

Description:
    Implementation of the Tic-tac-toe game with GUI and 3 levels of difficulty.
"""

import tkinter.messagebox
import tkinter
from turtle import RawTurtle, ScrolledCanvas
from functools import lru_cache

SCREENMIN = 0
SCREENMAX = 300
COMPUTER = 1
HUMAN = -1
PLAYERS = {1: "COMPUTER", -1: "HUMAN"}
AI_LEVELS = {"Dummy": 0, "Easy": 3, "Hard": 6}


class Board:
    """The board class that defines a Tic-tac-toe Board."""

    def __init__(self, board=None, screen=None):
        """
        When a board is constructed, you may want to make a copy of the board.
        This can be a shallow copy of the board because Turtle objects are
        Immutable from the perspective of a board object.
        """
        self.screen = screen
        if screen is None:
            if board:
                self.screen = board.screen

        self.items = []
        for i in range(3):
            row = []
            for j in range(3):
                if board is None:
                    row.append(Dummy())
                else:
                    row.append(board[i][j])

            self.items.append(row)

    def getscreen(self):
        """Accessor method for the screen"""
        return self.screen

    def __getitem__(self, index):
        """
        The getitem method is used to index into the board. It should
        return a row of the board. That row itself is indexable (it is just
        a list) so accessing a row and column in the board can be written
        board[row][column] because of this method.
        """
        return self.items[index]

    def __eq__(self, other):
        """Returns True if two boards represent exactly
           the same state and the same otherwise.

        This allows us to use lru_cache decorator.
        """
        if not isinstance(other, Board):
            return False

        if len(other.items) != 3:
            return False

        for item in other.items:
            if len(item) != 3:
                return False

        for i in range(3):
            for j in range(3):
                if self.items[i][j] != other.items[i][j]:
                    return False

        return True

    def __hash__(self):
        """A simple hash function."""
        result = 0
        for i in range(3):
            for j in range(3):
                result += (i + j) * self.items[i][j].eval()
        return result

    def reset(self):
        """ Reset the board.

        This method will mutate this board to contain all dummy
        turtles. This way the board can be reset when a new game
        is selected. It should NOT be used except when starting
        a new game.
        """
        self.screen.tracer(1)
        for i in range(3):
            for j in range(3):
                self.items[i][j].goto(-100, -100)
                self.items[i][j] = Dummy()

        self.screen.tracer(0)

    def eval(self):
        """Evaluate a board.

        This method should return an integer representing the
        state of the board. If the computer has won, return 1.
        If the human has won, return -1. Otherwise, return 0.
        """
        for i in range(3):
            row_sum = 0
            col_sum = 0
            for j in range(3):
                row_sum += self.items[i][j].eval()
                col_sum += self.items[j][i].eval()

            if abs(row_sum) == 3:
                return row_sum // 3

            if abs(col_sum) == 3:
                return col_sum // 3

        diag_sum_l = 0
        diag_sum_r = 0
        for i in range(3):
            diag_sum_l += self.items[i][i].eval()
            diag_sum_r += self.items[i][2 - i].eval()

        if abs(diag_sum_l) == 3:
            return diag_sum_l // 3

        if abs(diag_sum_r) == 3:
            return diag_sum_r // 3

        return 0

    def is_full(self):
        """Check if the board is full.

        Returns True if the board is completely filled up (no Dummy turtles).
        Otherwise, returns False.
        """
        for i in range(3):
            for j in range(3):
                if self.items[i][j].eval() == 0:
                    return False

        return True

    def draw_xos(self):
        """Draws the X's and O's of this board on the screen.  """
        for row in range(3):
            for col in range(3):
                if self[row][col].eval() != 0:
                    self[row][col].showturtle()
                    self[row][col].goto(col * 100 + 50, row * 100 + 50)

        self.screen.update()

    def available(self):
        """Return available (empty) cells."""
        return [
            (i, j)
            for j in range(3)
            for i in range(3)
            if isinstance(self.items[i][j], Dummy)
        ]

    def clone(self):
        """Return a copy of the board."""
        return Board(self)


class Dummy:
    """The Dummy object class.

    This class is just for placeholder objects when no move has been made
    yet at a position in the board. Having eval() return 0 is convenient
    when no move has been made.
    """

    def __init__(self):
        pass

    def eval(self):
        """Evaluation of Dummy object."""
        return 0

    def goto(self, x, y):
        """Leaving this untouched."""
        pass


class X(RawTurtle):
    """A class for representing Xs.

    In the X and O classes below the constructor begins by initializing the
    RawTurtle part of the object with the call to super().__init__(canvas).
    The super() call returns the class of the superclass (the class above the
    X or O in the class hierarchy).  In this case, the superclass is RawTurtle.
    Then, calling __init__ on the superclass initializes the part of the object
    that is a RawTurtle.
    """

    def __init__(self, canvas):
        if canvas is not None:
            super().__init__(canvas)
            self.hideturtle()
            self.getscreen().register_shape(
                "X",
                (
                    (-40, -36),
                    (-40, -44),
                    (0, -4),
                    (40, -44),
                    (40, -36),
                    (4, 0),
                    (40, 36),
                    (40, 44),
                    (0, 4),
                    (-40, 44),
                    (-40, 36),
                    (-4, 0),
                    (-40, -36),
                ),
            )
            self.pencolor("blue")
            self.shape("X")
            self.penup()
            self.speed(5)
            self.goto(-100, -100)

    def eval(self):
        """Evaluation of X object."""
        return COMPUTER


class O(RawTurtle):
    """A class for representing Xs.

    In the X and O classes below the constructor begins by initializing the
    RawTurtle part of the object with the call to super().__init__(canvas).
    The super() call returns the class of the superclass (the class above the
    X or O in the class hierarchy).  In this case, the superclass is RawTurtle.
    Then, calling __init__ on the superclass initializes the part of the object
    that is a RawTurtle.
    """

    def __init__(self, canvas):
        if canvas is not None:
            super().__init__(canvas)
            self.hideturtle()
            self.shapesize(5, 5, 10)
            self.fillcolor("white")
            self.pencolor("red")
            self.shape("circle")
            self.penup()
            self.speed(5)
            self.goto(-100, -100)

    def eval(self):
        """Evaluation of O object."""
        return HUMAN


@lru_cache(maxsize=6)
def minimax(player, board, depth=6):
    """The minimax function.

    The minimax function is given a player (1 = Computer, -1 = Human) and a
    board object. When the player = Computer, minimax returns the maximum
    value of all possible moves that the Computer could make. When the player =
    Human then minimax returns the minimum value of all possible moves the
    Human could make. Minimax works by assuming that at each move the Computer
    will pick its best move and the Human will pick its best move. It does this
    by making a move for the player whose turn it is, and then recursively
    calling minimax.  The base case results when, given the state of the board,
    someone has won or the board is full.
    """
    if board.eval():
        return board.eval()

    if board.is_full() or depth < 0:
        return 0

    if player == COMPUTER:
        best_move = -1
        for i, j in board.available():
            temp = board.clone()
            temp.items[i][j] = X(None)
            best_move = max(best_move, minimax(HUMAN, temp, depth - 1))
        return best_move

    if player == HUMAN:
        best_move = 1
        for i, j in board.available():
            temp = board.clone()
            temp[i][j] = O(None)
            best_move = min(best_move, minimax(COMPUTER, temp, depth - 1))
        return best_move


class TicTacToe(tkinter.Frame):
    """Tic-tac-toe GUI."""

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.paused = False
        self.stop = False
        self.running = False
        self.turn = HUMAN
        self.level = "Easy"
        self.locked = False
        self.build_window()

    def build_window(self):
        """Build a window."""
        canvas = ScrolledCanvas(self, 600, 600, 600, 600)
        canvas.pack(side=tkinter.LEFT)
        t = RawTurtle(canvas)
        screen = t.getscreen()
        screen.tracer(100000)

        screen.setworldcoordinates(SCREENMIN, SCREENMIN, SCREENMAX, SCREENMAX)
        screen.bgcolor("white")
        t.hideturtle()

        frame = tkinter.Frame(self)
        frame.pack(side=tkinter.RIGHT, fill=tkinter.BOTH)
        board = Board(None, screen)

        def draw_grid():
            screen.clear()
            screen.tracer(1000000)
            screen.setworldcoordinates(
                SCREENMIN, SCREENMIN, SCREENMAX, SCREENMAX
            )
            screen.bgcolor("white")
            screen.tracer(0)
            t = RawTurtle(canvas)
            t.hideturtle()
            t.penup()
            t.width(10)
            t.color("black")
            for i in range(2):
                t.penup()
                t.goto(i * 100 + 100, 10)
                t.pendown()
                t.goto(i * 100 + 100, 290)
                t.penup()
                t.goto(10, i * 100 + 100)
                t.pendown()
                t.goto(290, i * 100 + 100)

            screen.update()

        draw_grid()

        def new_game():
            # draw_grid()
            self.turn = HUMAN
            board.reset()
            self.locked = False
            screen.update()

        def start_handler():
            new_game()

        btn_start = tkinter.Button(
            frame, text="New Game", command=start_handler
        )
        btn_start.pack()

        tkvar = tkinter.StringVar(self)
        tkvar.set(self.level)

        def level_handler(*args):
            self.level = tkvar.get()

        lbl_level = tkinter.Label(frame, text="AI Level")
        lbl_level.pack()

        dd_level = tkinter.OptionMenu(
            frame, tkvar, command=level_handler, *AI_LEVELS
        )
        dd_level.pack()

        def quit_handler():
            self.master.quit()

        btn_quit = tkinter.Button(frame, text="Quit", command=quit_handler)
        btn_quit.pack()

        def computer_turn():
            """
            The locked variable prevents another event from being
            processed while the computer is making up its mind.
            """
            self.locked = True
            max_move = None

            # Call Minimax to find the best move to make.
            # After writing this code, the maxMove tuple should
            # contain the best move for the computer. For instance,
            # if the best move is in the first row and third column
            # then max_move would be (0,2).

            depth = AI_LEVELS[self.level]
            best_move = -float("inf")

            for i, j in board.available():
                temp = board.clone()
                temp.items[i][j] = X(None)
                value = minimax(HUMAN, temp, depth)
                if value > best_move:
                    best_move = value
                    row, col = i, j

            max_move = (row, col)
            row, col = max_move
            board[row][col] = X(canvas)
            self.locked = False

        def mouse_click(x, y):
            """Defines what happens on a mouse click."""
            if not self.locked:
                row = int(y // 100)
                col = int(x // 100)

                if board[row][col].eval() == 0:
                    board[row][col] = O(canvas)

                    self.turn = COMPUTER

                    board.draw_xos()

                    if not board.is_full() and not abs(board.eval()) == 1:
                        computer_turn()

                        self.turn = HUMAN

                        board.draw_xos()
                    else:
                        self.locked = True

                    if board.eval() == 1:
                        tkinter.messagebox.showwarning(
                            "Game Over", "Expectedly, Machine wins."
                        )
                    elif board.eval() == -1:
                        tkinter.messagebox.showerror(
                            "Game Over", "Suprisingly, Human wins."
                        )
                    elif board.is_full():
                        tkinter.messagebox.showinfo(
                            "Game Over", "It was a tie."
                        )

        screen.onclick(mouse_click)

        screen.listen()


def main():
    """Run the main function."""
    root = tkinter.Tk()
    root.title("Tic-tac-toe")
    application = TicTacToe(root)
    application.mainloop()


if __name__ == "__main__":
    main()
