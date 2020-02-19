from time import sleep
import datetime

def wait_for(condition):
    def safe_condition():
        try:
            return condition()
        except:
            return False

    while not safe_condition():
        sleep(1)


def wait_get(getter):
    while True:
        try:
            return getter()
        except:
            sleep(1)

def convertUrlToName(imgurl):
    return imgurl.split('.com/')[-1].replace('/', '_')

def timeshtamp():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")