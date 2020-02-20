from time import sleep
import datetime
import progressbar


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
