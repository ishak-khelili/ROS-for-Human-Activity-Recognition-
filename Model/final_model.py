# -*- coding: utf-8 -*-
"""Final_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1b9DAQo_zPJZXX4lq0o4w29A4ZfGvLw5w
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np

import matplotlib.pyplot as plt
# %matplotlib inline

from tensorflow import keras
from keras.utils import np_utils
from sklearn.model_selection import train_test_split

from keras import regularizers
from keras import Sequential
from keras.layers import Dense, Conv3D, BatchNormalization, Flatten, MaxPooling3D, Dropout, Activation

"""Preprocessing the data"""

#importing tensors of data 

with open('/content/drive/My Drive/New_dataset/X_23_arr.npy', 'rb') as f :

  X_23_arr = np.load(f)

with open('/content/drive/My Drive/New_dataset/X_40_arr.npy', 'rb') as f :

  X_40_arr = np.load(f)

with open('/content/drive/My Drive/New_dataset/X_31_arr.npy', 'rb') as f :

  X_31_arr = np.load(f)

with open('/content/drive/My Drive/New_dataset/X_36_arr.npy', 'rb') as f :

  X_36_arr = np.load(f)

print(X_23_arr.shape)
print(X_40_arr.shape)
print(X_31_arr.shape)
print(X_36_arr.shape)

# show samples of data:



img = X_23_arr[50,6,:,:,:]
plt.imshow(img)

#creating a tensor that holds all the data

X_data = np.concatenate((X_23_arr, X_31_arr, X_36_arr, X_40_arr))

print(X_data.shape)

#creating label tensor

X_labels=np.ones((len(X_data),),dtype = int)
X_labels[0:948]= 0
X_labels[948:1896] = 1
X_labels[1896:2844] = 2
X_labels[2844:3792] = 3

#Hot encoding the labels
Y_data = np_utils.to_categorical(X_labels)

#Spliting the dataset into training and test data

X_train, X_test, y_train, y_test = train_test_split(X_data, Y_data, test_size=0.2, random_state=42)

print("X_train shape :", X_train.shape)
print("X_test shape :", X_test.shape)

print("y_train shape :" , y_train.shape)
print("y_test shape :", y_test.shape)

"""Building the model"""

def build(classes):
  model = Sequential()

  model.add(Conv3D(16, kernel_size=(3, 3, 3),strides=(1,2,2), input_shape=(7,108,192,3)))
  model.add(Activation('relu'))
  model.add(Conv3D(32, kernel_size=(3, 3, 3),strides=(1,2,2)))
  model.add(Activation('relu'))
  model.add(MaxPooling3D(pool_size=(3, 3, 3)))
  
  
 # model.add(Conv3D(64, kernel_size=(3, 3, 3)))
 # model.add(Activation('relu'))
 # model.add(Conv3D(64, kernel_size=(3, 3, 3)))
 # model.add(Activation('relu'))
 # model.add(MaxPooling3D(pool_size=(3, 3, 3)))
  
  
  model.add(Flatten())

  model.add(Dense(512, activation='relu', kernel_regularizer=regularizers.l1(0.001)))
  model.add(Dropout(0.25))
  model.add(Dense(256, activation='relu',kernel_regularizer=regularizers.l1(0.001)))
  model.add(Dropout(0.25))
  model.add(Dense(128, activation='relu',kernel_regularizer=regularizers.l1(0.001)))
  

  model.add(Dense(classes, activation='softmax'))



  return model

model = build(4)
model.summary()

#Choosing optimizer

optimizer = keras.optimizers.Adam(learning_rate=0.001)
model.compile(
    optimizer,
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# training the model

EPOCHS=50

history = model.fit(X_train,y_train,batch_size=5,
    epochs=EPOCHS,
    verbose=1,
    validation_split=0.3
    
)

#Plotting results

def plot_learning_curve(history, epochs):
  #Plot training and validation accuracy values:
  epoch_range = range(1, epochs+1)
  plt.plot(epoch_range, history.history['accuracy'])
  plt.plot(epoch_range, history.history['val_accuracy'])
  plt.xlabel('Epochs')
  plt.ylabel('Acuuracy')
  plt.title('Accuracy curve')
  plt.legend(['Train','Val'],loc = 'upper left')
  plt.show()
  #plt.savefig('/content/drive/My Drive/Accuracy2.png')

  #Plot training and validation loss values :
  plt.plot(epoch_range, history.history['loss'])
  plt.plot(epoch_range, history.history['val_loss'])
  plt.axis([0, 50, 0, 3])
  plt.xlabel('Epochs')
  plt.ylabel('Loss')
  plt.title('Loss curve')
  plt.legend(['Train','Val'],loc = 'upper left')
  plt.show()
  #plt.savefig('/content/drive/My Drive/Loss2.png')

plot_learning_curve(history, EPOCHS)



# Evaluating the model on ne data

model.evaluate(X_test,y_test)

predictions = model.predict(X_test)

#This is an extraction of the percentage of random test data selection
#This percentage must be very low compared to the accuracy of test data so that we can say that our model is good enouph

import copy
test_labels_copy = copy.copy(y_test)       #Copy test labels into new list of test labels
np.random.shuffle(test_labels_copy)             #random the new list
hit_arrays = test_labels_copy == y_test    #compare the new with old and store reslts of comparison in hit_arrays as true or false
float(np.sum(hit_arrays)) / len(y_test)    #Sum the true hits and divide them by the over all data to get the percentage of true comparison

predictions.shape

predictions[10]

img = X_test[10,5,:,:,:]
plt.imshow(img)



model.save('/content/drive/My Drive')