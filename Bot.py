import random
import Constants
import msvcrt
from Graphics import PygameScreen as pg
from Constants import consts

class GenericBot:
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return hash(self) == hash(other)

    def open_moves(self, game):
        move_list = []
        for i in range(3):
            for j in range(3):
                if game.spaces[i][j] == consts.EMPTY:
                    move_list.append((i,j))
        return move_list

    def move(self, game):
        if game.draw():
            return
        next_move = self.think(game)
        game.update(next_move, self)

    def think(self, game):
        raise NotImplementedError


class RandomBot(GenericBot):
    def think(self, game):
        return random.choice(self.open_moves(game))

class Player(GenericBot):
    def think(self, game):
        move = pg.getMouseMove(self)
        if (move in self.open_moves(game)): return move
        else: return random.choice(self.open_moves(game))

class HardcodedPictureBot(GenericBot):
    def think(self, game):
        pass

class MiniMaxBot(GenericBot):
    def think(self, game):
        """
        Implement the minimax algorithm
            1. pick the max of your moves.
            2. the value of each of your moves is the min of your opponent's moves
               if you make that move

            Use this algorithm to implement a recursive algorithm.
            Base case: the game is decided. then it is worth a value.
                       recursive case: the min or max move.
            Each time we have to copy the board new so it's not contaminated
                (i.e. so no two recursive calls are editing the same data)
            so, algorithm:
                for each move:
                    hypothetically apply the move
                    recurse to hypothetically apply other move
        """
        moves = {}
        if len(self.open_moves(game)) == 9: return (0,0)

        val, move = self.recursion_solver(game, self.symbol)
        if not move: return random.choice(self.open_moves(game))
        elif random.random() < (consts.DIFFICULTY/100): return random.choice(self.open_moves(game))
        return move

    def recursion_solver(self, game, player):
        if game.no_winner():
            if player == self:
                best_score = -10**10
            else:
                best_score = 10**10
            best_move = None
            for move in self.open_moves(game):
                new_game = game.hypothetical(move, player)
                other_player = Constants.other_player(player)
                valueofmove, _ = self.recursion_solver(new_game, other_player)
                me_condition = player == self and valueofmove > best_score
                them_condition = player != self and valueofmove < best_score
                if me_condition or them_condition:
                    best_score = valueofmove
                    best_move = move
            return best_score, best_move
        else:
            if game.draw():
                return 0, None
            elif game.winner == self:
                return 1, None
            else:
                return -1, None
