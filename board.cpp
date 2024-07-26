#include "board.h"
int main(void) {

    Board b;
    std::list<std::pair<int, int>> peg_moves = b.moves_for_peg(1, 3);
}