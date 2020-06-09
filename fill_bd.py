import os
import sys
import types
import json
from memo.url_memo import memo
from common import Mark

from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets, uic


class Controller:
    def __init__(self, window):
        self.window = window
        memo.remove_urls([url for url in memo.getURLs() if memo.getUrlData(url)['mark'] == Mark.undefined.name])
            
        self.urls = memo.getURLs()
        self.position = 0
        self.loadImage()

        self.window.like.clicked.connect(self.like)
        self.window.like.clicked.connect(self.inc)

        self.window.dislike.clicked.connect(self.dislike)
        self.window.dislike.clicked.connect(self.inc)

        self.window.back.clicked.connect(self.dec)
        self.window.forward.clicked.connect(self.inc)

        self.window.save_current.clicked.connect(self.saveCurrent)

        def keyPressEvent(widget, event):
            key = event.key()
            if key == QtCore.Qt.Key_Space:
                return self.saveCurrent()
            if key == QtCore.Qt.Key_Up:
                return self.inc()
            if key == QtCore.Qt.Key_Down:
                return self.dec()
            if key == QtCore.Qt.Key_Right:
                self.like()
                return self.inc()
            if key == QtCore.Qt.Key_Left:
                self.dislike()
                return self.inc()

        self.window.root.keyPressEvent = types.MethodType(
            keyPressEvent, self.window.root)

    def getCurrentUrl(self):
        return self.urls[self.position]

    def getCurrentData(self):
        return memo.getUrlData(self.getCurrentUrl())

    def updateCurrent(self, data):
        new_data = self.getCurrentData()
        new_data.update(data)
        memo.upd_urls(
            {self.getCurrentUrl(): new_data})

    def setCurrent(self, data):
        memo.upd_urls({self.getCurrentUrl(): data})

    def loadImage(self):
        self.window.page.load(QtCore.QUrl(self.getCurrentUrl()))
        self.showStatus()

    def showStatus(self):
        data = self.getCurrentData()
        self.window.status.setText(json.dumps(data, indent=4, sort_keys=True))
        
        color = {
            Mark.undefined.name: 'background: grey',
            Mark.dislike.name: 'background: #ff557f',
            Mark.like.name: 'background: #00b800'
        }
        self.window.mark.setStyleSheet(color[data['mark']])
        self.window.prediction.setStyleSheet(color[data['prediction']])

    def inc(self):
        self.position += 1

        if self.position == len(self.urls):
            self.position = 0

        self.loadImage()

    def dec(self):
        self.position -= 1

        if self.position == -1:
            self.position = len(self.urls) - 1

        self.loadImage()

    def like(self):
        self.updateCurrent({'mark': 'like'})
        self.showStatus()

    def dislike(self):
        self.updateCurrent({'mark': 'dislike'})
        self.showStatus()

    def saveCurrent(self):
        try:
            parsed = json.loads(self.window.status.toPlainText())
            self.setCurrent(parsed)
            self.showStatus()
        except:
            pass


def main():
    app = QtWidgets.QApplication(sys.argv)
    path_ui = os.path.join(os.path.dirname(__file__), "fill_bd.ui")
    window = uic.loadUi(path_ui)
    Controller(window)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
