import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from search import *

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.resize(300, 600)
        self.statusBar().showMessage("Ready!")

        self.setWindowTitle("MacTorrentParser")

        parserWidget = TorrentParserWindow()        
        self.setCentralWidget(parserWidget)



class TorrentParserWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def torrentsParse(self):
        text = self.torrentEdit.text()
        self.torrentList = Search(text)
        for torrent in self.torrentList:
            self.list.addItem(torrent.text)

    def initUI(self):

        torrent = QLabel("Input torrent name")
        self.torrentEdit = QLineEdit()
        self.torrentEdit.setText("Adobe")

        parsingButton = QPushButton("Parsing")
        parsingButton.clicked.connect(self.torrentsParse)

        stopButton = QPushButton("Stop!")

        self.list = QListWidget()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(torrent, 1, 0)
        grid.addWidget(self.torrentEdit, 1, 1)

        grid.addWidget(parsingButton, 2, 0)
        grid.addWidget(stopButton, 2, 1)

        grid.addWidget(self.list, 3, 0, 5, 2)

        self.setLayout(grid)
        
def main():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec_()

if __name__ == '__main__':
    main()
