import datetime
from memo.url_memo import memo
import os
import urllib.request


def readURL(url):
    with urllib.request.urlopen(url) as response:
        return response.read()


def downloadimg(imgurl, folder):
    imgfilename = imgurl.split('.com/')[-1].replace('/', '_')

    full_path = folder + '/' + imgfilename
    if not os.path.isfile(full_path):
        print('load img:', imgfilename)
        with open(full_path, 'wb') as f:
            f.write(readURL(imgurl))
    else:
        print('skip img:', imgfilename)


for url in memo.getURLs():
    downloadimg(url, os.path.dirname(os.path.abspath(__file__)) + '/images')
