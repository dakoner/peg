from PyQt5 import QtWidgets, QtGui, QtCore
import solitaire

class PegGraphicsView(QtWidgets.QGraphicsView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Board = solitaire.Board()
        self.nx = len(self.Board.board[0])
        self.ny = len(self.Board.board)
        self.setScene(QtWidgets.QGraphicsScene())

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


        color = QtGui.QColor("red")
        pen = QtGui.QPen(color, 1)
        brush = QtGui.QBrush(color)
        for i in range(self.nx):
            for j in range(self.ny):

                if self.Board.board[i][j] == 1:
                    item = QtWidgets.QGraphicsEllipseItem(i*10 + 2.5, j*10 + 2.5, 5, 5)
                    item.setPen(pen)
                    item.setBrush(brush)
                    self.scene().addItem(item)
        self.scene().setSceneRect(QtCore.QRectF())
        self.scale(5,5)
        #self.fitInView(self.scene().sceneRect())
        