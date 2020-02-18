import datetime
from memo.url_memo import memo
import os
import urllib.request
import utils


def readURL(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


def downloadimg(imgurl, folder):
    imgfilename = utils.convertUrlToName(imgurl)

    full_path = folder + '/' + imgfilename
    if not os.path.isfile(full_path):
        print('load img:', imgfilename)
        with open(full_path, 'wb') as f:
            f.write(readURL(imgurl))
    else:
        print('skip img:', imgfilename)

def main():
    folder = os.path.dirname(os.path.abspath(__file__)) + '/images'

    if not os.path.isdir(folder):
       os.mkdir(folder) 

    for url in memo.getURLs():
        downloadimg(url, folder)

if __name__ == '__main__':
    main()