# -*- coding: utf-8 -*-
"""ftrain_NLP

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1-helNY_cPHWTkL_mTPxKwzEmI-Vu8lre
"""

from keras.utils import get_file
import tarfile
data_dir = get_file('aclImdb_v1.tar.gz', 'http://ai.stanford.edu/~amaas/data/sentiment/aclImdb_v1.tar.gz', cache_subdir = "datasets",hash_algorithm = "auto", extract = True, archive_format = "auto")

my_tar = tarfile.open(data_dir)
my_tar.extractall('./data/') # specify which folder to extract to
my_tar.close()

from glob import glob
import os,re,string
import numpy as np
PATH='./data/aclImdb/'
names = ['neg','pos']

def load_texts_labels_from_folders(path, folders):
    texts,labels = [],[]
    for idx,label in enumerate(folders):
        for fname in glob(os.path.join(path, label, '*.*')):
            texts.append(open(fname, 'r').read())
            labels.append(idx)
    
    return texts, np.array(labels).astype(np.int64)

x_train,y_train = load_texts_labels_from_folders(f'{PATH}train',names)
x_test,y_test = load_texts_labels_from_folders(f'{PATH}test',names)

def preprocess_reviews(reviews):
    tokens = re.compile("[.;:!#\'?,\"()\[\]]|(<br\s*/><br\s*/>)|(\-)|(\/)")
    
    return [tokens.sub("", line.lower()) for line in reviews]

x_train_clean = preprocess_reviews(x_train)
x_test_clean = preprocess_reviews(x_test)

x_train_clean[7]

y_train

import tensorflow as tf
from tensorflow import keras
tok = keras.preprocessing.text.Tokenizer()
tok.fit_on_texts(x_train_clean) 
X_train = tok.texts_to_sequences(x_train_clean)
X_test = tok.texts_to_sequences(x_test_clean)

#" ".join(map(str,X_train[0]))

lengths = [len(i) for i in X_train]
print(f'Max length of sentence: {max(lengths)}')
print(f'Average length of sentence: {np.mean(lengths)}')

from sklearn.model_selection import train_test_split
X_train = keras.preprocessing.sequence.pad_sequences(X_train,padding='post',maxlen=1000)
X_test = keras.preprocessing.sequence.pad_sequences(X_test,padding='post',maxlen=1000)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, random_state=42)
# X_train[7]

# build model
# input shape is the vocabulary count used for the movie reviews (10,000 words)
vocab_size = len(tok.word_index)+1

model = keras.Sequential()
model.add(keras.layers.Embedding(vocab_size, 16))
model.add(keras.layers.Dropout(0.1))
model.add(keras.layers.Conv1D(filters=16,kernel_size=2,padding='valid',activation='relu'))
model.add(keras.layers.GlobalAveragePooling1D())
model.add(keras.layers.Dropout(0.1))
model.add(keras.layers.Dense(32, activation='relu'))
model.add(keras.layers.Dropout(0.1))
model.add(keras.layers.Dense(1, activation='sigmoid'))

model.summary()

model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['acc'])

history = model.fit(X_train,y_train,
                    epochs=20,
                    validation_data=(X_val, y_val),
                    verbose=1, # print result every epoch
                    batch_size=512)

import matplotlib.pyplot as plt
def plot_loss(history):
  plt.plot(history.history['val_loss'],label="val loss")
  plt.plot(history.history['loss'],label="train loss")
  plt.xlabel('epoch')
  plt.ylabel('loss')

  plt.legend()
  plt.show()

plot_loss(history)

import matplotlib.pyplot as plt
def plot_loss(history):
  plt.plot(history.history['val_acc'],label="val loss")
  plt.plot(history.history['acc'],label="train loss")
  plt.xlabel('epoch')
  plt.ylabel('loss')

  plt.legend()
  plt.show()

plot_loss(history)

# Commented out IPython magic to ensure Python compatibility.
# %pwd
# %cd /content/drive/My Drive/assignment3/

model.save("./models/20834941_NLP_model.h5")