import signal
import time
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QLabel
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import random

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt rectangle colors - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 290
        self.height = 290
        self.initUI()
  
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
      
        # Set window background color
        self.setAutoFillBackground(True)
        #p = self.palette()
        #p.setColor(self.backgroundRole(), Qt.white)
        #self.setPalette(p)
      
        # Add paint widget and paint
        self.m = PaintWidget(self)
        #self.m.move(0,0)
        self.m.resize(self.width,self.height)
      
        self.show()
  
class PaintWidget(QWidget):
    def paintEvent(self, event):
        print("apint", time.time())
        qp = QPainter(self)
      
        qp.setPen(Qt.black)
        size = self.size()
      
        # Colored rectangles
        qp.setBrush(QColor(200, 0, 0))

        for i in range(7):
            for j in range(7):
                qp.drawEllipse(i*4*10+10, j*4*10+10, 20, 20)
      
      
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())