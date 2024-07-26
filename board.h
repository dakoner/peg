#include <iostream>
#include <list>
#include <algorithm>
const int nx = 7;
const int ny = 7;
class Board {
    int board[nx][ny] = {
        {2, 2, 1, 1, 1, 2, 2},
        {2, 2, 1, 1, 1, 2, 2},
        {1, 1, 1, 1, 1, 1, 1},
        {1, 1, 1, 0, 1, 1, 1},
        {1, 1, 1, 1, 1, 1, 1},
        {2, 2, 1, 1, 1, 2, 2},
        {2, 2, 1, 1, 1, 2, 2},
    };

    public:
    Board() {

    }
    Board(const Board& board_) {
        std::copy(&board_.board[0][0], &board_.board[0][0]+nx*ny,&board[0][0]);
    }

    int score() {
        int s = 0;
        for (auto i = 0; i < nx; i++) {
            for (auto j = 0; j < ny; j++) {
                if (board[i][j] == 1) s++;
            }
        }
        if (s == 1 && board[3][3] == 1) s=0;
        

        return s;
    }

    std::list<std::pair<int, int>> possible_moves() {
        std::list<std::pair<int, int>> moves;
        for (auto i = 0; i < nx; i++) {
            for (auto j = 0; j < ny; j++) {
                if (board[i][j] == 1) {
                    std::list<std::pair<int, int>> peg_moves = moves_for_peg(i, j);
                    moves.splice(moves.end(), peg_moves);
                }
            }
        }
        return moves;
    }

    std::list<std::pair<int, int>> moves_for_peg(int x, int y) {
        std::list<std::pair<int, int>> peg_moves;

        std::list<std::pair<int, int>> move_offsets = {{-2, 0}, {2, 0}, {0, -2}, {0, 2}};
        for (auto dxdy: move_offsets) {
            int new_x = x + dxdy.first;
            int new_y = y + dxdy.second;
            if (0 < new_x <= 6 && 0 <= new_y <= 6) {
                if (board[new_x][new_y] == 0) {
                    if (board[(x+new_x) / 2][(y+new_y) / 2] == 1) {
                        peg_moves.push_back(std::pair<int, int>(new_x, new_y));
                    }
                }
            }

        }
        return peg_moves;
    }

    void move(std::pair<std::pair<int, int>, std::pair<int, int>> move) {
        auto fxy = move.first;
        auto txy = move.second;
        auto from_x = fxy.first;
        auto from_y = fxy.second;
        auto to_x = txy.first;
        auto to_y = txy.second;

        board[from_x][from_y] = 0;
        board[to_x][to_y] = 1;
        board[(from_x + to_x)/2][(from_y+to_y)/2] = 0;


    }

    friend std::ostream& operator<<(std::ostream &out, Board const& board) {
        for (auto i = 0; i < nx; i++) {
            for (auto j = 0; j < ny; j++) {
                std::cout << board.board[i][j];
            }
            std::cout << std::endl;
        }
        return std::cout;
     }

};