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

from board import Board

class Solver:
    def __init__(self, callback=None):

        # Set of hashes of board positions. Used to skip boards that have been played already.
        self.boards_played = set()

        # Counters for statistical purposes.
        self.statistics = {'Games finished': 0, 'Boards skipped': 0}
        self.callback = callback

    def solve_recursive(self, board, move_memo=()):
        #print("Board=")
        #print(board)
        if self.callback:
            self.callback(board, move_memo)

        if hash(board) in self.boards_played:
            self.statistics['Boards skipped'] += 1
            return
        self.boards_played.add(hash(board))

        moves = board.possible_moves()

        # If there are no moves left
        if len(moves) == 0:
            #print("Finished with", board.score())
            self.statistics['Games finished'] += 1

            # If the game is solved
            if board.score() == 0:
                return move_memo
        else:
            for move in moves:
                #print("Consider move", move)
                result = self.solve_recursive(board.clone().move(move), [mm for mm in move_memo] + [move])
                if result:
                    return result


if __name__ == '__main__':
    s = Solver()
    moves_played = s.solve_recursive(Board())
    print(f"Finished {s.statistics['Games finished']} games! (skipped {s.statistics['Boards skipped']})")
    if moves_played:
        m = '\n'.join([f"{m[0][0]}, {m[0][1]} -> {m[1][0]}, {m[1][1]}" for m in moves_played])
        print(f"Solution found, moves:\n{m}")
