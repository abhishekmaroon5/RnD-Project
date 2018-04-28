# -*- coding: utf-8 -*-
"""VGG_CNN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R9Cre45BcaqefXSgihiBn6qLs57AhADc
"""

# Lets import that the requirements
import numpy as np
import sys
from keras.models import Sequential
from keras.layers import Dense
# from google.colab import files
from keras import applications
# In order to avoid overfiting we need dropout the layers.
from keras.layers import Dropout,Activation,Flatten
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator,img_to_array,array_to_img,load_img
#Generate batches of tensor image data with real-time data augmentation.The data will be looped over (in batches).

#Dependencies for the cnn
from keras.layers import Conv2D,MaxPooling2D,GlobalAveragePooling1D

! git clone --recursive https://github.com/abhishekmaroon5/dataset2



cd dataset2/

ls

import numpy
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
# from keras.utils import np_utils

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# Preprocess the data
datagen=ImageDataGenerator(rotation_range=25,
                       width_shift_range=0.2,
                       height_shift_range=0.2,
                       rescale=1./255,
                       shear_range=0.2,
                       zoom_range=0.2,
                       fill_mode='nearest',
                       horizontal_flip=True
                       )
# shear_range: Float. Shear Intensity (Shear angle in counter-clockwise direction as radians)
# zoom_range: Float or [lower, upper]. Range for random zoom. If a float

# create model
model = Sequential()
model.add(Conv2D(32, (3, 3), input_shape=( 250, 250,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
model.add(Conv2D(32, (3, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
model.add(Conv2D(64, (3, 3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2), dim_ordering="th"))
model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))
model.compile(loss='binary_crossentropy',optimizer="rmsprop",metrics=["accuracy"])

# Lets time to prepare the data
batch_size=16
# For training 
train_datagen=ImageDataGenerator(rotation_range=25,
                                 rescale=1./255,
                                 shear_range=0.2,
                                 zoom_range=0.2,
                                 fill_mode='nearest',
                                 horizontal_flip=True
                                )
# For Test_datagen we will only rescale the image
test_datagen=ImageDataGenerator(rescale=1./255)
train_generator=train_datagen.flow_from_directory('data/train',target_size=(250, 250),
        batch_size=batch_size,
        class_mode='binary')
test_generator=test_datagen.flow_from_directory('data/validate',target_size=(250, 250),
        batch_size=batch_size,
        class_mode='binary')





# # We have prepared a model.Its time to fit the model
# model.fit_generator(train_generator,
#                     steps_per_epoch=1000,
#                     epochs=5,
#                     validation_data=test_generator,
#                     validation_steps=800)
# model.save_weights('first_try.h5')



# Lets declare some varibles
img_width=200
img_height=200
train_data_dir='data/train'
validation_data_dir='data/validate'
nb_train_samples = 1072
nb_train_helmet = 550
nb_train_nonhelmet = 522
nb_validation_samples = 224
nb_val_helmet = 119
nb_val_nonhelmet = 105
epochs = 20
batch_size = 1
top_model_weights_path = 'weights.h5'
def save_bottlenack_features():
    datagen=ImageDataGenerator(rescale=1./255)
    
    # Lets build a VGG model...
    model=applications.VGG16(include_top=False,weights="imagenet")
    
    # Lets use images from our training dataset...
    
    generator = datagen.flow_from_directory(
        'data/train',
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    print("fit1")
    bottleneck_features_train = model.predict_generator(
        generator, nb_train_samples // batch_size)
    print("fit2")
    np.save(open('bottleneck_features_train.npy', 'wb'),
            bottleneck_features_train)
    # Lets use images from our testing dataset.
    generator = datagen.flow_from_directory(
        'data/validate',
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    print("fit3")
    bottleneck_features_validation = model.predict_generator(
        generator, nb_validation_samples // batch_size)
    np.save(open('bottleneck_features_validation.npy', 'wb'),
            bottleneck_features_validation)
     
save_bottlenack_features()

img_width=200
img_height=200
train_data_dir='data/train'
validation_data_dir='data/validate'
nb_train_samples = 1072
nb_train_helmet = 550
nb_train_nonhelmet = 522
nb_validation_samples = 224
nb_val_helmet = 119
nb_val_nonhelmet = 105
epochs = 200
batch_size = 1
top_model_weights_path = 'weights.h5'
def train_top_model():
      train_data = np.load(open('bottleneck_features_train.npy','rb'))
      train_labels = np.array([0] * (nb_train_helmet) + [1] * (nb_train_nonhelmet))
      validation_data = np.load(open('bottleneck_features_validation.npy','rb'))
      validation_labels = np.array([0] * (nb_val_helmet) + [1] * (nb_val_nonhelmet))
#       train_labels = np.array([0] * (train_samples // 2) + [1] * (train_samples // 2))      
      model = Sequential()
      model.add(Flatten(input_shape=train_data.shape[1:]))
      model.add(Dense(256, activation='relu'))
      model.add(Dropout(0.5))
      model.add(Dense(1, activation='sigmoid'))
      model.compile(optimizer='adam',
                    loss='binary_crossentropy', metrics=['accuracy'])
      print("fit")
      print(str(len(validation_data)))
      print(str(len(validation_labels)))
      print(str(len(train_data)))
      print(str(len(train_labels)))
      
#       model.fit_generator(train_data,
#                     steps_per_epoch=1000,
#                     epochs=20,
#                     validation_data=validation_data,
#                     validation_steps=800)
#       model.save_weights('first_try.h5')
      model.fit(train_data, train_labels,
            epochs=20,
            batch_size=1,
            validation_data=(validation_data, validation_labels))
      model.save_weights('weights.h5')
train_top_model()

