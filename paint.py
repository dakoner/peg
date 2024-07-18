import threading
import signal
import time
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from board import Board
from solver import Solver
from solver_thread import SolverThread

  
class PaintWidget(QtWidgets.QWidget):
    def __init__(self, board=Board(), parent=None):
        super().__init__(parent=parent)
        self.board = board
        self.setFixedSize(290, 290)
        layout=QtWidgets.QVBoxLayout()
        self.setLayout(layout)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        if self.board:
            for i in range(7):
                for j in range(7):
                    if self.board.board[i][j] == 1:
                        qp.setPen(QtCore.Qt.black)
                        qp.setBrush(QtCore.Qt.red)
                        qp.drawEllipse(i*4*10+10, j*4*10+10, 20, 20)
        else:
            qp.setPen(QtCore.Qt.black)
            qp.setBrush(QtCore.Qt.black)
            qp.drawRect(0, 0, self.width(), self.height())


        
                
    
        

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window background color
        self.setAutoFillBackground(True)
        
        # Add paint widget and paint
        self.m = PaintWidget(parent=self)
        #self.m.resize(self.width,self.height)
        self.setCentralWidget(self.m)

        self.solver = Solver(self.move_callback, self.done_callback)
        self.all_boards = []
        self.all_moves = []
        self.moves_played = self.solver.solve_recursive(Board())
        self.moves_played_reverse = list(reversed(self.moves_played))
        self.all_boards_reverse = list(reversed(self.all_boards))
        self.all_moves_reverse = list(reversed(self.all_moves))
        print(f"Finished {self.solver.statistics['Games finished']} games! (skipped {self.solver.statistics['Boards skipped']})")
        self.all_boards.reverse()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.start)
        #self.timer.start(1)
        self.timer.singleShot(100, self.start)

    def move_callback(self, board, moves):
        self.all_boards.append(board)

    def done_callback(self, board, moves):
        self.all_boards.append(None)
        self.all_moves.append(moves)

    def start(self):
        # try:
        #     moves = self.all_moves_reverse.pop()
        # except:
        #     return
        # else:
        #     b = Board()
        #     for move in moves:
        #         b.move(move)
        #         self.m.board = b
        #         self.m.repaint()
        #         self.m.update()
        #     print(b.score())
        board = self.all_boards_reverse.pop()
        self.m.board = board
        self.m.repaint()
        if board:
            self.timer.singleShot(10, self.start)
        else:
            self.timer.singleShot(100, self.start)


        # try:
        #     board = self.all_boards.pop()
        # except IndexError:
        #     return
        # else:
        #     self.m.board = board
        #     self.m.repaint()

        # try:
        #     move = self.moves_played_reverse.pop()
        # except IndexError:
        #     return
        # else:
        #     self.m.board.move(move)
        #     self.m.repaint()

        



if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
