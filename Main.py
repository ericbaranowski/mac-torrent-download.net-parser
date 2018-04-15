import time
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from search import *
import requests
from bs4 import BeautifulSoup


class MainWindow(QMainWindow):
    def __init__(self, parent = None):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setFixedSize(300, 600)
        #self.setWindowState(QtCore.Qt.Window) TODO 
        self.statusBar().showMessage("Ready!")

        self.setWindowTitle("MacTorrentParser")

        parserWidget = TorrentParserWindow(self)        
        self.setCentralWidget(parserWidget)


class Worker(QObject):

    sig_step = pyqtSignal(int)
    sig_done = pyqtSignal(int, bytes)

    def __init__(self, id: int, parent):
        super().__init__()
        self.__id = id
        self.__abort = False
        self.parent = parent
    
    @pyqtSlot()
    def work(self):
        time.sleep(0.1)
        self.sig_step.emit(self.__id)
        # torrentName = self.parent.torrentEdit.text()
        # torrentList = Search(torrentName)
        link = f"https://mac-torrent-download.net/page/1/{self.parent.torrentEdit.text()}"
        requestsall = requests.get(link, headers={'Connection': 'close'})

        app.processEvents() # Считываем с GUI инструкции
        self.sig_done.emit(self.__id, requestsall.content)
    
    def abort(self):
        print("Команда прирыва потока")
        self.__abort = True

class TorrentParserWindow(QWidget):
    NUM_THREADS = 1
    sig_abort_workers = pyqtSignal()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.torrent = QLabel("Input torrent name")

        self.torrentEdit = QLineEdit()
        self.torrentEdit.setText("Adobe")


        self.parsingButton = QPushButton("Parsing")
        self.parsingButton.clicked.connect(self.torrentsParse)
        
        self.stopButton = QPushButton("Stop!")
        self.stopButton.clicked.connect(self.abort_workers)
        self.stopButton.setDisabled(True)

        self.list = QListWidget()

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.torrent, 1, 0)
        grid.addWidget(self.torrentEdit, 1, 1)

        grid.addWidget(self.parsingButton, 2, 0)
        grid.addWidget(self.stopButton, 2, 1)

        grid.addWidget(self.list, 3, 0, 5, 2)

        self.setLayout(grid)

        self.__workers_done = None
        self.__threads = None


    def torrentsParse(self):
        print("torrentParse . . . ")
        self.parsingButton.setDisabled(True)
        self.stopButton.setEnabled(True)

        self.__workers_done = 0
        self.__threads = []
        for idx in range(self.NUM_THREADS):
            worker = Worker(idx, self)
            thread = QThread(self)
            thread.setObjectName('thread_' + str(idx))
            self.__threads.append((thread, worker)) 
            worker.moveToThread(thread)

            worker.sig_step.connect(self.on_worker_step)
            worker.sig_done.connect(self.on_worker_done)

            self.sig_abort_workers.connect(worker.abort)

            thread.started.connect(worker.work)
            thread.start()

    @pyqtSlot(int)
    def on_worker_step(self, worker_id: int):
        print("worker_id: {}".format(worker_id))

    @pyqtSlot(int, bytes)
    def on_worker_done(self, worker_id, html):
        print('Реквест завершился: {} '.format(worker_id))

        soup = BeautifulSoup(html, "html.parser")
        torrents_search = soup.find_all("a",{"rel":"bookmark"})
        print(html)
        self.__workers_done += 1
        if self.__workers_done == self.NUM_THREADS:
            self.parsingButton.setEnabled(True)
            self.stopButton.setDisabled(True)

    @pyqtSlot()
    def abort_workers(self):
        self.sig_abort_workers.emit()
        for thread, worker in self.__threads:
            thread.quit()
            thread.wait()

        print('Остановили процесс')
        

if __name__ == '__main__':
    app = QApplication([])
    gui = MainWindow()
    gui.show()
    sys.exit(app.exec_())
