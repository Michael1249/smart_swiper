import os
from memo.url_memo import memo
import numpy as np
from common import Mark, ROOT_PATH
from utils import execTask, getCorrelation, getMid

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


def calculateModelMetrics(y_pred, y_true):
    accuracy = 0
    false_like = 0
    false_dislike = 0
    for y_p, y_t in zip(y_pred, y_true):
        y_p = int(y_p > 0.5)
        if y_p == y_t:
            accuracy += 1
        elif y_p == Mark.like.value:
            false_like += 1
        else:
            false_dislike += 1

    def percent(val):
        return val / len(y_true)

    return percent(accuracy), percent(false_like), percent(false_dislike)


def compileModel(epochs=5000, seve_name = 'model'):
    (X, Y, _) = getDataSet()
    model = getModel()
    trainModel(model, X, Y, epochs)
    y_pred = [x[0] for x in model.predict(X)]

    accuracy, false_like, false_dislike = calculateModelMetrics(y_pred, Y)
    corelation = getCorrelation(y_pred, Y)
    realTolerance = getMid(Y)
    binTolerance = getMid([int(x > 0.5) for x in y_pred])
    modelTolerance = getMid(y_pred)

    metrics = {
        'real tolerance': realTolerance,
        'bin tolerance': binTolerance,
        'model tolerance': modelTolerance,
        'accuracy': accuracy,
        'correlation': corelation,
        'false_like': false_like,
        'false_dislike': false_dislike,
    }
    
    print("{:<16} {:<8}".format('METRIC','VALUE'))
    for key, val in metrics.items():
        print("{:<16} {:<8}".format(key, val))

    if not os.path.isdir(ROOT_PATH + '/models/'):
        os.mkdir(ROOT_PATH + '/models/') 

    model.save('models/' + seve_name + '.h5')    

# (X, Y, urls) = getDataSet()
#
# model = getModel()
#
# trainModel(model, X, Y, 5000)
#
# prediction = model.predict(X)
# new_data = [{'prediction': (Mark.like.name if x[0] > 0.38 else Mark.dislike.name)}
#             for x in prediction]
# memo.upd_urls(dict(zip(urls, new_data)))
#
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
#
# acc /= counter
# false_like /= counter
# false_dislike /= counter
# print('accuracy:', acc * 100)
# print('false like:', false_like * 100)
# print('false dislike:', false_dislike * 100)

if __name__ == '__main__':
    compileModel()