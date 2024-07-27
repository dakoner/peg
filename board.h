#include <optional>
#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <iostream>
#include <list>
#include <algorithm>
const int nx = 7;
const int ny = 7;

typedef std::pair<int, int> position_t;
typedef std::list<position_t> peg_moves_t;
typedef std::pair<position_t, position_t> move_t;
typedef std::list<move_t> moves_t;

class Board
{
public:
    int board_[nx][ny] = {
        {2, 2, 1, 1, 1, 2, 2},
        {2, 2, 1, 1, 1, 2, 2},
        {1, 1, 1, 1, 1, 1, 1},
        {1, 1, 1, 0, 1, 1, 1},
        {1, 1, 1, 1, 1, 1, 1},
        {2, 2, 1, 1, 1, 2, 2},
        {2, 2, 1, 1, 1, 2, 2},
    };

    Board();
    Board(const Board &board);

    const int board_at(int i, int j);

    int score();

    moves_t possible_moves();

    peg_moves_t moves_for_peg(int x, int y);

    void move(move_t move);

    friend std::ostream &operator<<(std::ostream &out, const Board& board);

    bool operator==(const Board board) const;

    struct BoardHash
    {
        size_t operator()(Board board) const
        {
            std::hash<int> hasher;
            size_t seed = 0;
            for (int i = 0; i < nx; i++)
            {
                for (int j = 0; j < ny; j++)
                {
                    seed ^= hasher(board.board_at(i, j) + 0x9e3779b9 + (seed << 6) + (seed >> 2));
                }
            }
            return seed;
        }
    };
};

class Solver
{
    Board board_;
    std::stack<Board> stack;
    std::unordered_set<Board, Board::BoardHash> boards_visited;
    std::unordered_map<Board, std::pair<move_t, Board>, Board::BoardHash> parent;

public:
    Solver(Board board);

    moves_t build_solution();

    moves_t solve_internal();

    void solve();
};
