import sys
import signal
from PyQt5.uic import loadUi

from PyQt5 import QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        loadUi("peg.ui", self)

class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)
        self.main_window = MainWindow()
        self.main_window.show()#showMaximized()


class QApplication(QtWidgets.QApplication):
    def __init__(self, *argv):
        super().__init__(*argv)
       
        
        self.window =  MainWindow()
        self.window.show()
        

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app = QApplication(sys.argv)
    sys.exit(app.exec())