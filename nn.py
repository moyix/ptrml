import os
import math
import keras
import numpy as np
import tensorflow as tf
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.callbacks import ModelCheckpoint

BATCH_SIZE = 131072

def build_model():
    strategy = tf.distribute.MirroredStrategy()
    with strategy.scope():
        model = Sequential()
        model.add(Dense(4096, input_dim=64))
        model.add(Activation('relu'))
        model.add(Dense(1))
        model.add(Activation('sigmoid'))

        opt = keras.optimizers.Adam(lr=0.0001)

        model.compile(loss='binary_crossentropy', optimizer=opt, metrics=['accuracy'])
        model.summary()

        return model

def train(model, data):
    all_x, all_y = data
    model.fit(all_x, all_y, epochs=10, batch_size=BATCH_SIZE, verbose=1)
    # Save model and weights
    model.save("weights.h5")

def load_ints(fname):
    if os.path.exists(fname + '.npy'):
        data = np.load(fname + '.npy')
    else:
        print(f"Loading data from {fname} for the first time, this will take a while... "
                "(future loads will be faster)")
        data = np.loadtxt(fname, dtype='uint64', converters = {0: lambda s: int(s,0)})
        np.save(fname, data)
    return np.unpackbits(data.byteswap().view('uint8')).reshape(data.shape[0], 64).astype('float32')

def load_data(pos, neg):
    x_pos = load_ints(pos)
    x_neg = load_ints(neg)
    labels = np.zeros(len(x_neg)+len(x_pos))
    labels[:len(x_pos)] = 1
    return np.vstack([x_pos, x_neg]), labels

def usage(args):
    print(f"{args[0]} <train|valid>")

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        usage(sys.argv)
        sys.exit(1)

    if sys.argv[1] == "train":
        data = load_data('train_pos.txt.gz', 'train_neg.txt.gz')
        model = build_model()
        train(model, data)
    elif sys.argv[1] == "valid":
        model = tf.keras.models.load_model('weights.h5')
        val_data = load_data('valid_pos.txt.gz', 'valid_neg.txt.gz')
        #val_dataset = tf.data.Dataset.from_tensor_slices((val_data[0], val_data[1]))
        results = model.evaluate(val_data[0], val_data[1], batch_size=10000)
        print("test loss, test acc:", results)
    else:
        usage(sys.argv)
        sys.exit(1)
