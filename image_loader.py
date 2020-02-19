import datetime
from memo.url_memo import memo
import os
import urllib.request
import utils
import progressbar


def readURL(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


def downloadimg(imgurl, folder):
    imgfilename = utils.convertUrlToName(imgurl)

    full_path = folder + '/' + imgfilename
    if not os.path.isfile(full_path):
        with open(full_path, 'wb') as f:
            f.write(readURL(imgurl))


def load():
    folder = os.path.dirname(os.path.abspath(__file__)) + '/images'

    if not os.path.isdir(folder):
        os.mkdir(folder)

    urls = memo.getURLs()
    bar = progressbar.ProgressBar(maxval=len(urls),
                                  widgets=['load images:', progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])

    bar.start()
    for i, url in enumerate(urls):
        downloadimg(url, folder)
        bar.update(i + 1)
    bar.finish()


if __name__ == '__main__':
    load()
