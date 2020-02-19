import pandas as pd
from memo.url_memo import memo
import numpy as np
from matplotlib import pyplot as plt

from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD

def getDataSet():
    X = memo.get_fields('encoding')
    Y = [[1] if x == 'like' else [0] for x in memo.get_fields('mark')]

    return np.array(X), np.array(Y)

(X, Y) = getDataSet()

model = Sequential()
model.add(Dense(90, input_dim=128))
model.add(Dense(60))
model.add(Dense(1))

sgd = SGD(lr=0.1)
model.compile(loss='mse', optimizer=sgd, metrics=['mse', 'accuracy'])
history = model.fit(X, Y, nb_epoch=10000, shuffle=True)

prediction = model.predict(X)
new_data = [{'prediction': ('like' if x[0] > 0.38 else 'dislike')} for x in prediction]
memo.upd_urls(dict(zip(memo.getURLs(), new_data)))

acc = 0
false_like = 0
false_dislike = 0
for x, y in zip(memo.get_fields('mark'), memo.get_fields('prediction')):
    if x == y:
        acc += 1
    elif y == 'like':
        false_like += 1
    else:
        false_dislike += 1
acc /= memo.size()
false_like /= memo.size()
false_dislike /= memo.size()
print('accuracy:', acc * 100)
print('false like:', false_like * 100)
print('false dislike:', false_dislike * 100)

plt.plot(history.history['accuracy'])
plt.show()