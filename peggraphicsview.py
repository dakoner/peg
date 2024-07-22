"""A brute force solver for the English (33 hole) variant of the peg solitaire board game."""
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import signal
import threading
from PyQt5.uic import loadUi

from typing import List, Tuple
from board import Board, IterativeSolver
SOLUTION = [((5, 3), (3, 3)), ((4, 5), (4, 3)), ((6, 4), (4, 4)), ((6, 2), (6, 4)), ((4, 3), (4, 5)), ((4, 6), (4, 4)), ((4, 2), (6, 2)), ((4, 0), (4, 2)), ((3, 4), (5, 4)), ((6, 4), (4, 4)), ((3, 6), (3, 4)), ((3, 4), (5, 4)), ((3, 2), (3, 4)), ((3, 0), (3, 2)), ((3, 2), (5, 2)), ((6, 2), (4, 2)), ((2, 4), (4, 4)), ((5, 4), (3, 4)), ((2, 6), (2, 4)), ((2, 3), (2, 5)), ((1, 2), (3, 2)), ((2, 0), (2, 2)), ((0, 4), (2, 4)), ((3, 4), (1, 4)), ((0, 2), (0, 4)), ((0, 4), (2, 4)), ((2, 5), (2, 3)), ((2, 3), (2, 1)), ((4, 2), (2, 2)), ((2, 1), (2, 3)), ((1, 3), (3, 3))]

class CustomDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("HELLO!")

        QBtn = QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QtWidgets.QVBoxLayout()
        self.sequence = QtWidgets.QLineEdit(str(SOLUTION))
        self.sequence.setMaxLength(len(str(SOLUTION))+5)
        self.layout.addWidget(self.sequence)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)

class PegGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_items = {}
        self.setScene(QtWidgets.QGraphicsScene())
        self.solver = IterativeSolver()
        self.update_board()
        self.draw_lines()
        self.scene().setSceneRect(QtCore.QRectF())
        self.scale(5,5)
        
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.showTime)        

    def showTime(self):
        if self.solver.stack:
            solution = self.solver.solve_iterative()
            self.update_board()
            if solution:
                print("Solution found")
                print(list(solution))
                self.timer.stop()

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


    def update_board(self):
        
        self.nx = len(self.solver.board.board[0])
        self.ny = len(self.solver.board.board)
        for i in range(self.nx):
            for j in range(self.ny):
                if (i,j) not in self.board_items:
                    item = QtWidgets.QGraphicsEllipseItem(i*10 + 2.5, j*10 + 2.5, 5, 5)
                    color = QtGui.QColor("red")
                    pen = QtGui.QPen(color, 1)
                    brush = QtGui.QBrush(color)
                    item.setPen(pen)
                    item.setBrush(brush)
                    self.scene().addItem(item)
                    self.board_items[i,j] = item
                if self.solver.board.board[i][j] == 1:
                    self.board_items[i,j].show()
                elif self.solver.board.board[i][j] == 0:
                    self.board_items[i,j].hide()
                elif self.solver.board.board[i][j] == 2:
                    self.board_items[i,j].hide()

    def action(self, event):
        if event.objectName() == "actionNext":
            # self.timer.stop()
            # if len(self.solver.stack):
            #     solution = self.solver.solve_iterative()
            #     self.update_board()
            #     if solution:
            #         print("Solution found", solution)
            # else:
            #     print("Stack empty")
            if self.step < len(self.solution):
                self.solver.board.move(self.solution[self.step])
                self.step += 1
                self.update_board()
        elif event.objectName() == 'actionStart':
            self.timer.start(0)
        elif event.objectName() == 'actionRestart':
            self.timer.stop()
            self.solver = IterativeSolver()
            self.update_board()
        elif event.objectName() == 'actionSequence':
            self.timer.stop()
                
            dlg = CustomDialog(self)
            if dlg.exec():
                print("Success!")
                print(dlg.sequence.text())
                self.solution = eval(dlg.sequence.text())
                self.step = 0
                self.solver.board = Board()
                self.update_board()

            else:
                print("Cancel!")

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