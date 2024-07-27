#include "board.h"
#include <vector>
#include <optional>
#include <unordered_set>
#include <unordered_map>
#include <stack>
#include <iostream>
#include <list>
#include <algorithm>

Board::Board()
{
}
Board::Board(const Board &board)
{
    std::copy(&board.board_[0][0], &board.board_[0][0] + nx * ny, &board_[0][0]);
}
const int Board::board_at(int i, int j)
{
    return board_[i][j];
}

int Board::score()
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

moves_t Board::possible_moves()
{
    moves_t moves;
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

peg_moves_t Board::moves_for_peg(int x, int y)
{
    peg_moves_t peg_moves;

    peg_moves_t move_offsets = {{-2, 0}, {2, 0}, {0, -2}, {0, 2}};
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
                    peg_moves.push_back(position_t(new_x, new_y));
                }
            }
        }
    }
    return peg_moves;
}

void Board::move(move_t move)
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

std::ostream &operator<<(std::ostream &out, const Board& board)
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

bool Board::operator==(const Board board) const
{
    for (int i = 0; i < nx; i++)
    {
        for (int j = 0; j < ny; j++)
        {
            if (board_[i][j] != board.board_[i][j])
                return false;
        }
    }
    return true;
}

Solver::Solver(Board board) : board_(board)
{
    stack.push(board);
}

moves_t Solver::build_solution()
{
    moves_t solution;
    while (true)
    {
        if (!parent.contains(board_))
        {
            solution.reverse();
            return solution;
        }
        auto move_and_board = parent[board_];
        solution.push_back(move_and_board.first);
        board_ = move_and_board.second;
    }
}

moves_t Solver::solve_internal()
{
    board_ = stack.top();
    stack.pop();
    if (!boards_visited.contains(board_))
    {
        boards_visited.insert(board_);
        auto moves = board_.possible_moves();
        if (moves.size() == 0)
        {
            auto score = board_.score();
            if (score == 0) {
                return build_solution();
            }
        }
        for (auto move : moves)
        {
            Board b(board_);
            b.move(move);
            auto p = make_pair(move, board_);
            auto i = make_pair(b, p);
            parent.insert(i);
            stack.push(b);
        }
    }
    return moves_t();
}

void Solver::solve()
{
    moves_t result;
    while (true)
    {
        result = solve_internal();
        if (result.size())
            break;
    }
    for(auto move: result) {
        std::cout << "Move: " << move.first.first << "," << move.first.second << " " << move.second.first << "," << move.second.second << std::endl;
    }
}

int main(void)
{

    Board b;
    Solver s(b);
    s.solve();
}