#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <iostream>
#include <list>
#include <algorithm>
const int nx = 7;
const int ny = 7;

class Board
{
    int board_[nx][ny] = {
        {2, 2, 1, 1, 1, 2, 2},
        {2, 2, 1, 1, 1, 2, 2},
        {1, 1, 1, 1, 1, 1, 1},
        {1, 1, 1, 0, 1, 1, 1},
        {1, 1, 1, 1, 1, 1, 1},
        {2, 2, 1, 1, 1, 2, 2},
        {2, 2, 1, 1, 1, 2, 2},
    };

public:
    Board()
    {
    }
    Board(const Board &board)
    {
        std::copy(&board.board_[0][0], &board.board_[0][0] + nx * ny, &board_[0][0]);
    }
    const int board_at(int i, int j)
    {
        return board_[i][j];
    }
    int score()
    {
        int s = 0;
        for (auto i = 0; i < nx; i++)
        {
            for (auto j = 0; j < ny; j++)
            {
                if (board_[i][j] == 1)
                    s++;
            }
        }
        if (s == 1 && board_[3][3] == 1)
            s = 0;

        return s;
    }

    std::list<std::pair<std::pair<int, int>, std::pair<int, int>>> possible_moves()
    {
        std::list<std::pair<std::pair<int, int>, std::pair<int, int>>> moves;
        for (auto x = 0; x < nx; x++)
        {
            for (auto y = 0; y < ny; y++)
            {
                if (board_[x][y] == 1)
                {
                    auto peg_moves = moves_for_peg(x, y);
                    for (auto peg_move : peg_moves)
                        moves.push_back(std::make_pair(std::make_pair(x, y), peg_move));
                }
            }
        }
        return moves;
    }

    std::list<std::pair<int, int>> moves_for_peg(int x, int y)
    {
        std::list<std::pair<int, int>> peg_moves;

        std::list<std::pair<int, int>> move_offsets = {{-2, 0}, {2, 0}, {0, -2}, {0, 2}};
        for (auto dxdy : move_offsets)
        {
            int new_x = x + dxdy.first;
            int new_y = y + dxdy.second;
            if (0 <= new_x && new_x <= 6 && 0 <= new_y && new_y <= 6)
            {
                if (board_[new_x][new_y] == 0)
                {
                    if (board_[(x + new_x) / 2][(y + new_y) / 2] == 1)
                    {
                        peg_moves.push_back(std::pair<int, int>(new_x, new_y));
                    }
                }
            }
        }
        return peg_moves;
    }

    void move(std::pair<std::pair<int, int>, std::pair<int, int>> move)
    {
        auto fxy = move.first;
        auto txy = move.second;
        auto from_x = fxy.first;
        auto from_y = fxy.second;
        auto to_x = txy.first;
        auto to_y = txy.second;

        board_[from_x][from_y] = 0;
        board_[to_x][to_y] = 1;
        board_[(from_x + to_x) / 2][(from_y + to_y) / 2] = 0;
    }

    friend std::ostream &operator<<(std::ostream &out, Board const &board)
    {
        for (auto i = 0; i < nx; i++)
        {
            for (auto j = 0; j < ny; j++)
            {
                std::cout << board.board_[i][j];
            }
            std::cout << std::endl;
        }
        return std::cout;
    }
};


struct BoardHash
{
    size_t operator()(Board& board) const
    {
        std::hash<int> hasher;
        size_t seed = 0;
        for (int i = 0; i < nx; i++)
        {
            for (int j = 0; j < ny; j++)
            {
                seed ^= hasher(board.board_at(i, j) + 0x9e3779b9 + (seed<<6) + (seed>>2));
            }
        }
        return seed;
    }
};

class Solver
{
    Board board_;
    std::stack<std::pair<Board, std::pair<std::pair<int, int>, std::pair<int, int>>>> stack;
         std::unordered_set<Board> boards_visited;
    //     std::unordered_map<Board, std::pair<std::pair<int, int>, std::pair<int, int>>, Board> parent;

    // public:
    //     Solver(Board board) : board_(board)
    //     {
    //     }

    //     std::list<std::pair<std::pair<int, int>, std::pair<int, int>>> build_solution()
    //     {
    //     }

    //     std::list<std::pair<std::pair<int, int>, std::pair<int, int>>> solve_internal()
    //     {
    //         auto board_and_move = stack.top();
    //         auto board = board_and_move.first;
    //         stack.pop();
    //         if (!boards_visited.contains(board))
    //         {
    //             boards_visited.insert(board);
    //             auto moves = board.possible_moves();
    //             if (moves.size() == 0)
    //             {
    //                 auto score = board.score();
    //                 if (score == 0)
    //                     return build_solution();
    //             }
    //             for (auto move : moves)
    //             {
    //                 Board b(board);
    //                 b.move(move);
    //                 parent.insert(std::make_pair(b, make_pair(move, board)));
    //                 stack.push(std::make_pair(b, move));
    //             }
    //         }
    //     }

    //     void solve()
    //     {
    //         while (true)
    //         {
    //             auto result = solve_internal();
    //             std::cout << result;
    //         }
    //     }
};
