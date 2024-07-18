#!/usr/bin/env python3
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""A brute force solver for the English (33 hole) variant of the peg solitaire board game."""
import math
from board import Board
import time
class Solver:
    def __init__(self):
        # Set of hashes of board positions. Used to skip boards that have been played already.
        self.boards_visited = set()

    def build_solution(self, board, parent):
        solution = []
        while True:
            try:
                move, board = parent[board]
                solution.append(move)
            except KeyError:
                return reversed(solution)
            
    def solve_iterative(self, board):
        stack = [(None, board)]
        parent = {}
        while len(stack):
            move, board = stack.pop()
            if board not in self.boards_visited:
                self.boards_visited.add(board)

                moves = board.possible_moves()
                if len(moves) == 0:
                    score = board.score()
                    if score == 0:
                        return self.build_solution(board, parent)
                        
                for move in moves:
                    b = board.clone().move(move)
                    parent[b] = (move, board)
                    stack.append((move, b))


if __name__ == '__main__':
    s = Solver()
    moves_played = s.solve_iterative(Board())
    print(list(moves_played))
    
