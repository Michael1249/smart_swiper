import datetime
from memo.url_memo import memo
import os
import urllib.request
import utils
from utils import execTask


def readURL(url):
    try:
        with urllib.request.urlopen(url) as response:
            return response.read()
    except:
        return None


def downloadimg(imgurl, folder):
    imgfilename = utils.convertUrlToName(imgurl)

    full_path = folder + '/' + imgfilename
    if not os.path.isfile(full_path):
        data = readURL(imgurl)
        if data != None:
            with open(full_path, 'wb') as f:
                f.write(data)


def load():
    folder = os.path.dirname(os.path.abspath(__file__)) + '/images'

    if not os.path.isdir(folder):
        os.mkdir(folder)

    urls = memo.getURLs()

    def Task(progress):
        for i, url in enumerate(urls):
            downloadimg(url, folder)
            progress.update(i + 1)

    execTask(name='load images:', size=len(urls), task=Task)


if __name__ == '__main__':
    load()
