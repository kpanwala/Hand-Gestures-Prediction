# -*- coding: utf-8 -*-
"""Kaggle gestures

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FBSZ4KkmBxkLIpwbPYHpQm4ZZkmgOAXA
"""

from google.colab import files
files.upload()

!mkdir ~p ~/.kaggle
!cp kaggle.json ~/.kaggle/

!chmod 600 ~/.kaggle/kaggle.json

!kaggle datasets download -d gti-upm/leapgestrecog

from zipfile import ZipFile
file_name="leapgestrecog.zip"

with ZipFile(file_name,'r') as zip:
  zip.extractall()
  print('done')

import os 
os.getcwd()

# cd ".."

from sklearn.datasets import load_files
import numpy as np

train_dir = "./leapGestRecog/0"
test_dir = "./leapgestrecog/leapGestRecog/09"

# train_dir1 = "./leapGestRecog/09"
# test_dir1 = "./leapgestrecog/leapGestRecog/01"



def load_dataset(path):
    data = load_files(path)
    files = np.array(data['filenames'])
    targets = np.array(data['target'])
    target_labels = np.array(data['target_names'])
    return files,targets,target_labels

tp = train_dir + "0"
x_train, y_train, target_labels = load_dataset(tp)

for i in range(1,9):
  tp = train_dir + str(i)
  x_train1, y_train1, target_labels1 = load_dataset(tp)
  x_train = np.concatenate((x_train, x_train1), axis=None)
  y_train= np.concatenate((y_train, y_train1), axis=None)
  target_labels = np.concatenate((target_labels, target_labels1), axis=None)


len(x_train)

# x_train1, y_train1,target_labels1 = load_dataset(train_dir)
# x,y,z = load_dataset(train_dir1)

"""

x_train = np.concatenate((x_train1, x), axis=None)
y_train= np.concatenate((y_train1, y), axis=None)
target_labels = np.concatenate((target_labels1, z), axis=None)

"""

x_test, y_test,_ = load_dataset(test_dir)
print('Loading complete!')

print('Training set size : ' , x_train.shape[0])
print('Testing set size : ', x_test.shape[0])

no_of_classes = len(np.unique(y_train))
no_of_classes

print(y_train[0:10])

from keras.utils import np_utils
y_train = np_utils.to_categorical(y_train,no_of_classes)
y_test = np_utils.to_categorical(y_test,no_of_classes)
y_train[0] # Note that only one element has value 1(corresponding to its label) and others are 0.


x_test,x_valid = x_test[700:],x_test[:700]
y_test,y_vaild = y_test[700:],y_test[:700]
print('Vaildation X : ',x_valid.shape)
print('Vaildation y :',y_vaild.shape)
print('Test X : ',x_test.shape)
print('Test y : ',y_test.shape)

x_train[0]

# We just have the file names in the x set. Let's load the images and convert them into array.
from keras.preprocessing.image import array_to_img, img_to_array, load_img

def convert_image_to_array(files):
    images_as_array=[]
    for file in files:
        # Convert to Numpy Array
        images_as_array.append(img_to_array( load_img(file,target_size=(100,100)) ))
    return images_as_array

x_train = np.array(convert_image_to_array(x_train))
print('Training set shape : ',x_train.shape)

x_valid = np.array(convert_image_to_array(x_valid))
print('Validation set shape : ',x_valid.shape)

x_test = np.array(convert_image_to_array(x_test))
print('Test set shape : ',x_test.shape)

print('1st training image shape ',x_train[0].shape)

print('1st training image as array',x_train[0]) # don't worry if you see only 255s..
# there are elements will other values too :p

# time to re-scale so that all the pixel values lie within 0 to 1
x_train = x_train.astype('float32')/255
x_valid = x_valid.astype('float32')/255
x_test = x_test.astype('float32')/255
x_train[0]

from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D
from keras.layers import Activation, Dense, Flatten, Dropout
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras import backend as K

# del(model)

model = Sequential()
model.add(Conv2D(filters = 16, kernel_size = 2,input_shape=(100, 100, 3),padding='same'))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters = 32,kernel_size = 2,activation= 'relu',padding='same'))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters = 64,kernel_size = 2,activation= 'relu',padding='same'))
model.add(MaxPooling2D(pool_size=2))

model.add(Conv2D(filters = 128,kernel_size = 2,activation= 'relu',padding='same'))
model.add(MaxPooling2D(pool_size=2))

model.add(Dropout(0.3))
model.add(Flatten())
model.add(Dense(30))
model.add(Activation('relu'))
model.add(Dropout(0.4))
model.add(Dense(10,activation = 'softmax'))
model.summary()


model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

print('Compiled!')

batch_size = 32

checkpointer = ModelCheckpoint(filepath = 'cnn_from_gest_recog.hdf5', verbose = 1, save_best_only = True)

# simple model with approx arround 89% accuracy

history = model.fit(x_train,y_train,
        batch_size = 32,
        epochs=20,
        validation_data=(x_valid, y_vaild),
        callbacks = [checkpointer],
        verbose=2, shuffle=True)


model.load_weights('cnn_from_gest_recog.hdf5')

score = model.evaluate(x_test, y_test, verbose=0)
print('\n', 'Test accuracy:', score[1])


from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.grid_search import GridSearchCV
from keras.models import Sequential
from keras.layers import Dense

def build_classifier(optimizer):
  model = Sequential()
  model.add(Conv2D(filters = 16, kernel_size = 2,input_shape=(100, 100, 3),padding='same'))
  model.add(Activation('relu'))
  model.add(MaxPooling2D(pool_size=2))
  model.add(Conv2D(filters = 32,kernel_size = 2,activation= 'relu',padding='same'))
  model.add(MaxPooling2D(pool_size=2))
  model.add(Conv2D(filters = 64,kernel_size = 2,activation= 'relu',padding='same'))
  model.add(MaxPooling2D(pool_size=2))
  model.add(Conv2D(filters = 128,kernel_size = 2,activation= 'relu',padding='same'))
  model.add(MaxPooling2D(pool_size=2))
  model.add(Dropout(0.3))
  model.add(Flatten())
  model.add(Dense(30))
  model.add(Activation('relu'))
  model.add(Dropout(0.4))
  model.add(Dense(10,activation = 'softmax'))
  model.compile(loss='categorical_crossentropy',optimizer=optimizer,metrics=['accuracy'])
  return model

model = KerasClassifier(build_fn = build_classifier)

parameters = {'batch_size': [25, 32],
              'epochs': [20, 50],
              'optimizer': ['adam', 'rmsprop']}

# model with approx arround 99.22% accuracy using grid search view
grid_search = GridSearchCV(estimator = model,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 10)

grid_search = grid_search.fit(x_train, y_train)