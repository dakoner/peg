"""A brute force solver for the English (33 hole) variant of the peg solitaire board game."""
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import signal
import threading
from PyQt5.uic import loadUi

from typing import List, Tuple
from board import Board
from solver_iterative import Solver

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
        #self.timer.start(5)
        self.timer.timeout.connect(self.showTime)
        self.solver = Solver()

    def showTime(self):
        if self.solver.stack:
            solution = self.solver.solve_iterative()
            self.update_board(self.solver.board.board)
            if solution:
                print("Solution found")
                print(list(solution))
                self.timer.timeout.disconnect(self.showTime)


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
        for i in range(self.nx):
            for j in range(self.ny):
                if self.board[i][j] == 1:
                    self.board_items[i,j].show()
                elif self.board[i][j] == 0:
                    self.board_items[i,j].hide()

    def action(self, event):
            if event.objectName() == "actionNext":                
                if len(self.solver.stack):
                    solution = self.solver.solve_iterative()
                    self.update_board(self.solver.board.board)
                    if solution:
                        print("Solution found", solution)
                else:
                    print("Stack empty")
            elif event.objectName() == 'actionStart':
                self.timer.start(1)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        loadUi("peg.ui", self)
        self.toolBar.actionTriggered.connect(self.graphicsView.action)
        
class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)
        self.main_window = MainWindow()
        self.main_window.show()#showMaximized()




if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = QApplication(sys.argv)
    sys.exit(app.exec())