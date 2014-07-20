#Interface elements
from PyQt5 import QtCore, QtWidgets
#Distorm elements...


class Window(QtWidgets.QWidget):
    '''
    Root window

    Need to implement all the ui elements first, then start connecting them

    Or should I do it all programatically and worry about UI later...
    Seems like a waste of time to replicate a UI when there's no worker code, but
    it also seems like fully replicating the UI would help.
    '''
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.view = AnalysisBar(self)
        self.button = QtWidgets.QPushButton('Clear View', self)
        self.button.clicked.connect(self.handleClearView)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.button)

    def handleClearView(self):
        self.view.scene().clear()

class AnalysisBar(QtWidgets.QGraphicsView):
    '''
    Analysis bar
    '''
    def __init__(self, parent):
        QtWidgets.QGraphicsView.__init__(self, parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))

    def mousePressEvent(self, event):
        self._start = event.pos()

    def mouseReleaseEvent(self, event):
        start = QtCore.QPointF(self.mapToScene(self._start))
        end = QtCore.QPointF(self.mapToScene(event.pos()))
        self.scene().addItem(
            QtWidgets.QGraphicsLineItem(QtCore.QLineF(start, end)))
        for point in (start, end):
            text = self.scene().addSimpleText(
                '(%d, %d)' % (point.x(), point.y()))
            text.setBrush(QtCore.Qt.red)
            text.setPos(point)

    def set_location(self, location):
        pass
    def set_state(self, state):
        pass
