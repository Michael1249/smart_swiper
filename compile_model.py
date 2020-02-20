import pandas as pd
from memo.url_memo import memo
import numpy as np
from common import Mark
from utils import execTask

from model import getModel
from keras.callbacks import callbacks


def getDataSet():
    X = []
    Y = []
    urls = []

    for x, y, url in zip(memo.get_fields('encoding'), memo.get_fields('mark'), memo.getURLs()):
        mark = Mark[y]
        if mark != Mark.undefined and x != []:
            X += [x]
            Y += [mark.value]
            urls += [url]

    return np.array(X), np.array(Y), urls


def trainModel(model, x, y, epochs):
    def Task(progress):
        def updProgress(i, _):
            progress.update(i + 1)

        return model.fit(x, y, epochs=epochs, shuffle=True, verbose=0, callbacks=[
            callbacks.LambdaCallback(on_epoch_end=updProgress)
        ])

    return execTask(name='train model:', size=epochs, task=Task)

def compileModel(epochs = 1000, seve_name = 'model'):
    (X, Y, _) = getDataSet()
    model = getModel()
    trainModel(model, X, Y, 1000)

    model.save(seve_name + '.h5')    

# (X, Y, urls) = getDataSet()

# model = getModel()

# trainModel(model, X, Y, 1000)

# prediction = model.predict(X)
# new_data = [{'prediction': (Mark.like.name if x[0] > 0.38 else Mark.dislike.name)}
#             for x in prediction]
# memo.upd_urls(dict(zip(urls, new_data)))

# acc = 0
# false_like = 0
# false_dislike = 0
# counter = 0
# for x, y in zip(memo.get_fields('mark'), memo.get_fields('prediction')):
#     if Mark[x] != Mark.undefined and Mark[y].value != Mark.undefined:
#         counter += 1
#         if x == y:
#             acc += 1
#         elif y == Mark.like.name:
#             false_like += 1
#         else:
#             false_dislike += 1

# acc /= counter
# false_like /= counter
# false_dislike /= counter
# print('accuracy:', acc * 100)
# print('false like:', false_like * 100)
# print('false dislike:', false_dislike * 100)

if __name__ == '__main__':
    compileModel()