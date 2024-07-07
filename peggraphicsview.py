"""A brute force solver for the English (33 hole) variant of the peg solitaire board game."""
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import signal
import threading
from PyQt5.uic import loadUi

from typing import List, Tuple
from board import Board


class PegGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = Board()
        self.nx = len(self.board.board[0])
        self.ny = len(self.board.board)
        self.setScene(QtWidgets.QGraphicsScene())
        self.draw_lines()
        self.draw_pips()
        self.scene().setSceneRect(QtCore.QRectF())
        self.scale(5,5)
        #self.fitInView(self.scene().sceneRect())
        
    
        self.lock = threading.Lock()
        
        self.lock.acquire()

        self.timer = QtCore.QTimer()
        self.timer.start(100)
        self.timer.timeout.connect(self.showTime)

        self.solver = Solver(self)
        self.solver.start()

    def showTime(self):
        if self.lock.locked():
            self.lock.release()


    def draw_lines(self):
        color = QtGui.QColor("black")
        pen = QtGui.QPen(color, 1)

        for i in range(self.nx+1):
            item = QtWidgets.QGraphicsLineItem(i*10, 0, i*10, self.ny*10)
            item.setPen(pen)
            self.scene().addItem(item)

        for j in range(self.ny+1):
            item = QtWidgets.QGraphicsLineItem(0, j*10, self.nx*10, j*10)
            item.setPen(pen)
            self.scene().addItem(item)

    def draw_pips(self):
        color = QtGui.QColor("red")
        pen = QtGui.QPen(color, 1)
        brush = QtGui.QBrush(color)
        self.board_items = {}
        for i in range(self.nx):
            for j in range(self.ny):

                if self.board.board[i][j] != 2:
                    item = QtWidgets.QGraphicsEllipseItem(i*10 + 2.5, j*10 + 2.5, 5, 5)
                    item.setPen(pen)
                    item.setBrush(brush)
                    self.scene().addItem(item)
                    self.board_items[i,j] = item
                    if self.board.board[i][j] == 0:
                        item.hide()

    def update_board(self, board):
        self.board = board
        #print(self.board)
        print(self.board_items.keys())
        for i in range(self.nx):
            for j in range(self.ny):
                
                if self.board[i][j] == 1:
                    self.board_items[i,j].show()
                elif self.board[i][j] == 0:
                    self.board_items[i,j].hide()


class Solver(threading.Thread):
    def __init__(self, graphics_view, group=None, target=None, name=None,
                 args=(), kwargs=None):
        super().__init__(group=group, target=target, 
			             name=name)

        self.graphics_view = graphics_view

        # Set of hashes of board positions. Used to skip boards that have been played already.
        self.boards_played = set()

        # Counters for statistical purposes.
        self.statistics = {'Games finished': 0, 'Boards skipped': 0}

    def run(self):
        #while True:
        self.board = Board()
        moves_played = self.solve_recursive(self.board)
        print(f"Finished {self.statistics['Games finished']} games! (skipped {self.statistics['Boards skipped']})")
        if moves_played:
            m = '\n'.join([f"{m[0][0]}, {m[0][1]} -> {m[1][0]}, {m[1][1]}" for m in moves_played])
            print(f"Solution found, moves:\n{m}")

    def solve_recursive(self, board, move_memo=()):
        self.graphics_view.lock.acquire()
        self.graphics_view.update_board(board.board)
        if hash(board) in self.boards_played:
            self.statistics['Boards skipped'] += 1
            return
        self.boards_played.add(hash(board))

        moves = board.possible_moves()

        # If there are no moves left
        if len(moves) == 0:
            print("Game finished, score:", board.score())
            self.statistics['Games finished'] += 1

            # If the game is solved
            if board.score() == 0:
                return move_memo
        else:
            for move in moves:
                print("Try move", move)
                result = self.solve_recursive(board.clone().move(move), [mm for mm in move_memo] + [move])
                if result:
                    print("Got result", result)
                    return result



class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("peg.ui", self)
        
        
class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)
        self.main_window = MainWindow()
        self.main_window.show()#showMaximized()




if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    sys.exit(app.exec())