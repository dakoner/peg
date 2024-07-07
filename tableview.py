import signal
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data
        self.nopip = QtGui.QPixmap("icon1.png")
        self.pip = QtGui.QPixmap("icon2.png")

    def data(self, index, role):

        if role == Qt.DecorationRole:
            d = self._data[index.row()][index.column()]
            if d > 0:
                return self.pip
            else:
                return self.nopip
        else:
            return QtCore.QVariant()

    def rowCount(self, index):
        return len(self._data)

    def columnCount(self, index):
        return len(self._data[0])

class TableView(QtWidgets.QTableView):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setShowGrid(False)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().hide()
        self.verticalHeader().hide()
        self.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.setFocusPolicy(QtCore.Qt.NoFocus)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.table = TableView()

        data = [
          [4, 9, 2],
          [1, 0, 0],
          [3, 5, 0],
          [3, 3, 2],
          [7, 8, 9],
        ]

        self.model = TableModel(data)
        self.table.setModel(self.model)
        self.setCentralWidget(self.table)

      
if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL)

    app=QtWidgets.QApplication(sys.argv)
    window=MainWindow()
    window.show()
    sys.exit(app.exec_())