from time import sleep

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

