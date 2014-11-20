from PySide.QtCore import *
from PySide.QtGui import *
import sys
import app

class PipeUI(QWidget):

    def __init__(self):
        QWidget.__init__(self)

        # Layouts
        qvBoxLayout = QVBoxLayout()
        qhBoxLayout = QHBoxLayout ()

        # Buttons
        self.runHoudiniButton = QPushButton()
        self.runMayaButton = QPushButton()



        # Tab
        tabWidget = QTabWidget ()

        tabWidget.addTab (self.runHoudiniButton, 'Name')
        tabWidget.addTab (self.runMayaButton, 'Name2')


        qvBoxLayout.addWidget (tabWidget)


        # Housini
        self.houdiniIcon = QIcon("icon/houdini.png")
        self.runHoudiniButton.setIcon(self.houdiniIcon)

        # Maya
        mayaIcon = QIcon("icon/maya.png")
        self.runMayaButton.setIcon(mayaIcon)

        # Add widgets to layout

        # qhBoxLayout.addWidget(self.runHoudiniButton)
        # qhBoxLayout.addWidget(self.runMayaButton)

        # qvBoxLayout.addLayout (qhBoxLayout)

        # Set layout of main window
        self.setStyleSheet("QWidget {color: rgb(240,240,240); background-color: rgb(24,24,24)}"
                            "QLabel {color: rgb(240,240,240); background-color: rgb(24,24,24)}"
                            "QPushButton {background-color: rgb(24,24,24)}"
                            "QLineEdit {color: rgb(240,240,240); background-color: rgb(24,24,24)}"
                            "QTreeView {color: rgb(240,240,240); background-color: rgb(24,24,24)}")

        # self.iconComboBox = QtGui.QComboBox()
        # self.iconComboBox.addItem(self.houdiniIcon, "good")
        # self.showMinimized()




        # self.windowChange = QEvent.WindowStateChange
        # print self.windowChange
        # if QEvent.Resize:
        #     print 'Window Changed'
        # if self.changeEvent (:
        #     print 'stateChanfg'

        self.setLayout(qvBoxLayout)
        self.setWindowTitle("Pipe")
        self.resize(300,800)
        self.setFocus()
        self.createTrayIcon ()





    def keyPressEvent (self, e):
        if e.key() == Qt.Key_Escape:
            self.close()




    def changeEvent (self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() != Qt.WindowMinimized:
                if QCoreApplication.instance().minimizeToTray():
                    QTimer.singleShot(250, self, SLOT('hide()'))
        return super (PipeUI, self).changeEvent (event)

        # QCoreApplication.processEvents ()
        # self.hide ()
        # event.ignore ()

    # def changeEvent (self, e):
    #     if e.type() == QEvent.WindowStateChange:
    #         if self.isMinimized():
    #             self.close ()

    # def changeEvent (self, event):
    #     if event.type() == QEvent.WindowStateChange:
    #         if self.windowState() & Qt.WindowMinimized:
    #             event.ignore()
    #             self.close()
    #             return super (PipeUI, self).changeEvent(event)


    ### Working. But using this on closeEvent is stupid.
    # def closeEvent (self, event):
    #     event.ignore ()
    #     self.hide()
    #     self.trayIcon.showMessage ('Running', 'Running in the background.')


    def test (self):
        self.show()
        print "aaaaaa"

    def closeFunc (self):
        self.close ()

    def createTrayIcon(self):
        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction('restore', self.test)
        self.trayIconMenu.addAction('close', self.closeFunc)
        # self.trayIconMenu.addAction(self.restoreAction)
        # self.trayIconMenu.addSeparator()
        # self.trayIconMenu.addAction(self.quitAction)

        self.trayIcon = QSystemTrayIcon(self.houdiniIcon)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.show()



application = QApplication(sys.argv)
dialog = PipeUI()
dialog.show()
application.exec_()