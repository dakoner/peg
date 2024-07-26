#include "board.h"
#include <vector>
int main(void) {

    Board b;
    auto moves = b.possible_moves();
    auto move = moves.front();
    std::cout
            << "(" << move.first.first << "," << move.first.second << ") "
            <<  "(" <<move.second.first << "," << move.second.second << ")"
            << std::endl;
    std::cout << b << std::endl;
    b.move(move);
    std::cout << b << std::endl;
    std::cout << b.board_at(0,0) << std::endl;
    std::unordered_set<Board, BoardHash> boards_visited;

}