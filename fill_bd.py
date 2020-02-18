import os
import sys
from memo.url_memo import memo

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, uic

class Controller:
    def __init__(self, window):
        self.window = window
        self.urls = memo.getURLs()
        self.position = 0
        self.loadImage()

        self.window.like.clicked.connect(self.like)
        self.window.like.clicked.connect(self.inc)

        self.window.dislike.clicked.connect(self.dislike)
        self.window.dislike.clicked.connect(self.inc)

        self.window.back.clicked.connect(self.dec)
        self.window.forward.clicked.connect(self.inc)

    def getCurrentUrl(self):
        return self.urls[self.position]

    def loadImage(self):
        self.window.page.load(QtCore.QUrl(self.getCurrentUrl()))
        self.showStatus()
    
    def showStatus(self):
        self.window.status.setText(str(memo.getUrlData(self.getCurrentUrl())))

    def inc(self):
        self.position += 1

        if self.position == len(self.urls):
            self.position = 0
        
        self.loadImage()
    
    def dec(self):
        self.position -= 1

        if self.position == -1:
            self.position = len(self.urls) -1
        
        self.loadImage()

    def like(self):
        memo.upd_urls({self.getCurrentUrl(): {'mark' : 'like'}})
        self.showStatus()

    def dislike(self):
        memo.upd_urls({self.getCurrentUrl(): {'mark' : 'dislike'}})
        self.showStatus()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    path_ui = os.path.join(os.path.dirname(__file__), "bd_filler.ui")
    window = uic.loadUi(path_ui)
    controller = Controller(window)
    window.show()
    sys.exit(app.exec_())