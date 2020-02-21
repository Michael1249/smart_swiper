from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import SGD


def getModel():
    model = Sequential()
    model.add(Dense(90, input_dim=128))
    model.add(Dense(60))
    model.add(Dense(1))

    sgd = SGD(lr=0.1)
    model.compile(loss='mse', optimizer=sgd, metrics=['mse', 'accuracy'])

    return model
