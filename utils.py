from time import sleep
import datetime
import progressbar
import math


def waitFor(condition):
    def safe_condition():
        try:
            return condition()
        except:
            return False

    while not safe_condition():
        sleep(1)


def lateGet(getter):
    while True:
        try:
            return getter()
        except:
            sleep(1)


def convertUrlToName(imgurl):
    return imgurl.split('.com/')[-1].replace('/', '_')


def timeshtamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")


def execTask(name, task, size = 100):
    bar = progressbar.Bar('=', '[', ']')
    progress = progressbar.ProgressBar(maxval=size,
                           widgets=[name, bar, ' ', progressbar.Percentage()])

    progress.start()
    progress.update(0)
    result = task(progress)
    progress.finish()
    return result

def getMid(x):
        return sum(x) / len(x)

def getDev(x):
    mid = getMid(x)
    return math.sqrt(1 / (len(x) - 1) * sum([(xi - mid) ** 2 for xi in x]))

def getCorrelation(a, b):
    mid_a = getMid(a)
    mid_b = getMid(b)
    dev_a = getDev(a)
    dev_b = getDev(b)
    return (1 / (len(a) - 1)) * sum([(x - mid_a) / dev_a * (y - mid_b) / dev_b for x, y in zip(a, b)])