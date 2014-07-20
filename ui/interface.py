#!/usr/bin/env python3
'''
PyQt user interface and some other bits that need to be moved...
'''

from PyQt5.QtWidgets import (QApplication,
    QMainWindow, QToolBar, QWidget, QFileDialog, 
    QVBoxLayout, QHBoxLayout, QFrame)
from PyQt5 import QtCore
from analysisbar import AnalysisBar

#from ODP.core import AnalaysisDatabase
#from ODP.plugins import *

class AnalaysisDatabase():
    '''
    All data areas should call functions here to get their most recent data
    on expose/draw events or register callbacks when the data is updated.  It
    Keeps the user interface de-coupled from the data... so you can drive it
    programatically without having PyQt5 installed at all.

    I'm probably going to separate data per window/pane in to separate data piles
    This way, I can version those tables and tell whether we need to update a
    widget or not.

    This needs to move out of the interface file and in to somewhere else, but
    I just started.  Doesn't make any sense to move it until I have something working
    though, because it needs to be installable before non-relative imports make sense.

    Hopefully I find the staying power this time.
    Everyone has wanted to do this at least once, but nobody ever finishes.
    '''
    self.filename = ''
    self.dbname = ''


class Window(QMainWindow):
    def __init__(self):
        '''
        No I'm not trying to make all windows pop-out-able.
        Not as customizable a workflow, but it's probably the default for a reason.

        Operating under the assumption that the application will be run maximized.
        Not trying to handle resize until later in case it gets pulled across multiple screens.
        '''
        super(Window, self).__init__()
        self.setWindowTitle("OpenDisassembler")
        self.info_database = AnalaysisDatabase()
        self.create_ui()

    def create_ui(self):
        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.create_menubar()
        self.create_toolbar()

        mainLayout = QVBoxLayout()
        mainWidget = QFrame()
        mainWidget.setLayout(mainLayout)
        self.setCentralWidget(mainWidget)

        '''
        I'm used to Gtk...  So, this whole auto-widget noise is a little new.
        Using QFrame's seems like a better idea than subclassing QWidget, even
        though that is probably what I'm supposed to do.

        I might change QFrame to QWidget later...
        '''
        self.create_analysisbar()
        self.create_split_pane(mainLayout)
        self.createBottomPanel()

        self.statusBar().showMessage("Interface loaded")

    def create_menubar(self):
        '''
        Debating about how closely to replicate IDA here...
        '''
        menu = self.menuBar().addMenu('&File')
        menu.addAction("&New...", self.newFile, "Ctrl+N")
        menu.addAction("&Open...", self.openFile, "Ctrl+O")
        menu.addAction("&Recent", self.recentFile)
        menu.addAction("&Save...", self.saveFile, "Ctrl+S")
        menu.addAction("&Close", self.closeFile)
        menu.addAction("E&xit", QApplication.instance().quit, "Ctrl+Q")
        menu = self.menuBar().addMenu('&Edit')
        menu = self.menuBar().addMenu('&Search')
        menu = self.menuBar().addMenu('&Jump')
        menu = self.menuBar().addMenu('&View')
        menu = self.menuBar().addMenu('&Debugger')
        menu = self.menuBar().addMenu('&Options')
        menu = self.menuBar().addMenu('&Windows')
        menu = self.menuBar().addMenu('&Help')
        menu.addAction("&About", self.about)
        
    def create_toolbar(self):
        '''
        Generic toolbar placeholder

        Debating about how closely to replicate IDA here...
        '''
        self.toolBar = QToolBar()
        self.addToolBar(QtCore.Qt.ToolBarArea(QtCore.Qt.TopToolBarArea), self.toolBar)
        #I moved on.  Waiting for icon theme blob disambiguation or switching to monochrome icons.
        #Most of the callbacks here would be implemented much later anyway.

    def create_analysisbar(self):
        '''
        This one will certainly be a custom widget...
        '''
        pass

    def create_split_pane(self, mainLayout):
        #Use QSplitter here
        self.create_left_panel()
        self.create_right_panel()

    def create_left_panel(self):
        self.create_function_pane()
        self.create_graph_overview_pane()

    def create_function_pane(self):
        pass
    def create_graph_overview_pane(self):
        pass

    def create_right_panel(self):
        self.create_decompilation_tab()
        self.create_graph_tab()
        self.create_hex_tab()
        self.create_structures_tab()
        self.create_enums_tab()
        self.create_imports_tab()
        self.create_exports_tab()

    def create_decompilation_tab(self):
        pass
    def create_graph_tab(self):
        pass
    def create_hex_tab(self):
        pass
    def create_structures_tab(self):
        pass
    def create_enums_tab(self):
        pass
    def create_imports_tab(self):
        pass
    def create_exports_tab(self):
        pass

    def createBottomPanel(self):
        pass

    def createNotificationBar(self):
        pass

    #Menu callbacks
    def newFile(self):
        pass
    def openFile(self):
        '''
        Grabbing a list of parsers should happen here

        Hard coded linux/mac only here...  Sorry Windows.
        '''
        fname = QFileDialog.getOpenFileName(self, 'Open file', 
                '/home')
        print(fname)

        '''
        f = open(fname, 'r')
        
        with f:        
            data = f.read()
            self.textEdit.setText(data) 
        '''
    def saveFile(self):
        pass
    def recentFile(self):
        pass
    def closeFile(self):
        '''
        Save or not dialog if not perm setting.
        '''
        pass
    def about(self):
        '''
        Just a cheezy about Window with a donate/website URL
        '''
        pass

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    window = Window()
    window.show()

    sys.exit(app.exec_())