from typing import List, Tuple

class Board(object):
    def __init__(self, board=None):
        # 0 = empty, 1 = occupied, 2 = invalid
        self.board = board or [
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
            [1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 0, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1],
            [2, 2, 1, 1, 1, 2, 2],
            [2, 2, 1, 1, 1, 2, 2],
        ]

    def __hash__(self):
        return hash(tuple([tuple(row) for row in self.board]))

    def clone(self):
        # Ca. 2x faster than copy.deepcopy()
        board_copy = [[peg for peg in row] for row in self.board]
        return Board(board_copy)

    def score(self) -> int:
        # Count all pegs
        s = 0
        for peg in [p for row in self.board for p in row]:
            s += 1 if peg == 1 else 0

        # If there is only one peg left and it is in the center, the score is 0.
        if s == 1 and self.board[3][3] == 1:
            s = 0

        return s

    def possible_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        moves = []  # Format: ((from x, from y), (to x, to y))

        # For each board position
        for x, row in enumerate(self.board):
            for y, peg in enumerate(row):
                # If occupied by a peg
                if peg == 1:
                    # Find valid moves for this peg
                    peg_moves = self.moves_for_peg(x, y)

                    moves.extend([((x, y), move) for move in peg_moves])

        return moves

    def moves_for_peg(self, x, y) -> List[Tuple[int, int]]:
        assert 0 <= x <= 6
        assert 0 <= y <= 6

        peg_moves = []

        # x, y offsets for moves towards top, bottom, left, and right
        move_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2)]

        for (dx, dy) in move_offsets:
            new_x = x + dx
            new_y = y + dy

            # If new position is inside the board
            if 0 <= new_x <= 6 and 0 <= new_y <= 6:
                # If the new position is free
                if self.board[new_x][new_y] == 0:
                    # If there is a peg next to the current peg in the move's direction
                    if self.board[(x + new_x) // 2][(y + new_y) // 2] == 1:
                        peg_moves.append((new_x, new_y))

        return peg_moves

    def move(self, move: Tuple[Tuple[int, int], Tuple[int, int]]):
        (from_x, from_y), (to_x, to_y) = move

        # Delete peg from old position
        assert self.board[from_x][from_y] == 1
        self.board[from_x][from_y] = 0
        # Place peg at new position
        assert self.board[to_x][to_y] == 0
        self.board[to_x][to_y] = 1
        # Delete peg in between
        assert self.board[(from_x + to_x) // 2][(from_y + to_y) // 2] == 1
        self.board[(from_x + to_x) // 2][(from_y + to_y) // 2] = 0

        return self

    def __repr__(self):
        s = []
        for j in range(len(self.board[0])-1):
            for i in range(len(self.board)-1):
                s += str(self.board[i][j])
            s += '\n'

        return ''.join(s)
    