from PyQt5 import QtWidgets, QtGui


class PegGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        pen = QtGui.QPen(QtGui.QColor("red"), 3)
        item = QtWidgets.QGraphicsLineItem(0, 0, 100, 100)
        item.setPen(pen)
        self.setScene(QtWidgets.QGraphicsScene())
        self.scene().addItem(item)
        