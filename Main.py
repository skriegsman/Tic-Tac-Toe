import sys
import Bot
import Graphics
import Constants
import random
import time
import tkinter as tk
from Constants import consts
from copy import deepcopy

class TicTacToe:
    def __init__(self, p1, p2):
        self.game = None
        self.p1 = p1
        self.p2 = p2

    def run(self):
        self.game = GameBoard.NewBoard()
        self.game.turn_on_screen()

        if random.choice([True, False]) and consts.RANDOMSTART:
            first = self.p2
            other = self.p1
        else :
            first = self.p1
            other = self.p2

        #Game Loop
        while self.game.no_winner():
            first.move(self.game)
            first, other = other, first
        time.sleep(2.5)

class GameBoard:
    def __init__(self, spaces):
        self.spaces = spaces
        self.screen = None
        self.winner = None
        self.loser = None

    def turn_on_screen(self):
        self.screen = Graphics.PygameScreen()

    @classmethod
    def NewBoard(cls, spaces = None, screen=None):
        spaces = spaces or [[consts.EMPTY for _ in range(3)] for _ in range(3)]
        board = cls(spaces)
        if screen:
            board.screen = screen
            screen.reset()
        return board

    def update(self, move, player):
        i, j = move
        if isinstance(player, str):
            self.spaces[i][j] = player
        else:
            self.spaces[i][j] = player.symbol
            if self.screen:
                self.screen.draw(move, player)

    def draw(self):
        game_over = all([cell!=consts.EMPTY for row in self.spaces for cell in row])
        no_winner = self.winner is None
        return game_over and no_winner

    def set_winner(self, winner):
        self.winner = winner
        self.loser = Constants.other_player(self.winner)

    def vert_winner(self):
        spaces_by_col = [[self.spaces[i][j] for i in range(3)] for j  in range(3)]
        for col in spaces_by_col:
            if Constants.all_same(col):
                self.set_winner(col[0])
                return True
        return False

    def row_winner(self):
        for row in self.spaces:
            if Constants.all_same(row):
                self.set_winner(row[0])
                return True
        return False

    def diag_winner(self):
        diag1 = [(0,0), (1,1), (2,2)]
        diag2 = [(0,2), (1,1), (2,0)]
        diags = [diag1, diag2]
        for diag in diags:
            if Constants.all_same([self.spaces[i][j] for i,j in diag]):
                self.set_winner(self.spaces[1][1])
                return True
        return False

    def no_winner(self):
        if self.vert_winner() or self.row_winner() or self.diag_winner():
            return False
        elif self.draw():
            return False
        return True

    def hypothetical(self, move, player):
        new_spaces = deepcopy(self.spaces)
        newgame = GameBoard.NewBoard(new_spaces)
        newgame.update(move, player)
        return newgame

if __name__ == "__main__":
    if len(sys.argv) > 1:
        consts.FPS = int(sys.argv[1])

    while not consts.ENDSESSION:
        if consts.AIGAME:
            p1 = Bot.MiniMaxBot(consts.X)
        else:
            p1 = Bot.Player(consts.X)
        p2 = Bot.MiniMaxBot(consts.O)

        TicTacToe(p1,p2).run()
