import signal
import time
import sys
from PyQt5 import QtWidgets, QtGui, QtCore

from board import Board
from solver import Solver


  
class PaintWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setFixedSize(290, 290)
        layout=QtWidgets.QVBoxLayout()
        self.setLayout(layout)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.setPen(QtCore.Qt.black)
        size = self.size()
      
        # Colored rectangles
        qp.setBrush(QtCore.Qt.red)

        for i in range(7):
            for j in range(7):
                qp.drawEllipse(i*4*10+10, j*4*10+10, 20, 20)
      
      
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        #self.setFixedSize(self.width, self.height)
        #self.setLayout(self.layout)


        # Set window background color
        self.setAutoFillBackground(True)
        
      
        # Add paint widget and paint
        self.m = PaintWidget(self)
        #self.m.resize(self.width,self.height)
        self.setCentralWidget(self.m)


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
