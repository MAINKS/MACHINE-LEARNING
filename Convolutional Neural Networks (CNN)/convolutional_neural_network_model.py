# -*- coding: utf-8 -*-
"""Convolutional_Neural_Network_Model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eP85hjmw9_gJjxul5gFMrEgDDTDAEcmI

# Convolutional Neural Network

Classification of I/P image as Dog or Cat based on the trained data in CNN Using Deep Learning algortihm.



The Implementation of CNN is done on Jupyter Notebook as due to large number of dataset & size = megabytes of data with 8,000 sample images.


To run and view the implementation, we need to use the Jupyter Notebook in CNN.

### Importing the libraries
"""

import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
tf.__version__

#ImageDataGenarator class of image submodule of preprocessing module from keras library is used to preprocess the dataset

#Only tensorflow and keras library required to implement deep learning CNN algo

"""## Part 1 - Data Preprocessing

### Preprocessing the Training set
"""

#Data preprocessing in this section is not on the Tabular integral value dataset,
#But preprocessing of the dataset having Images within it for classification using CNN

#TRY : We can also combine NLP+Deep Learning Through Keras lib to build a text model, give i/p as text & o/p as response from CNN

#We're going to implement transformation on our image dataset , so as to avoid Overfitting - 98% accuracy on Train set, 43% on test set
#If we won't apply transformation on the image dataset, there will be huge difference in accuracy of training to test predictions.
#Transformations are geometrical shifts - rotate , zoom , stretch , flips and series of transformation
#Also called Augmentation of dataset - augment the variety of image train-set , so as model won't overlearn  / overtrain.

#train_datagen is object of ImageDataGenerator class of Keras Library
train_datagen = ImageDataGenerator(rescale = 1./255,       #Importing all Transform features to apply & preserving in train_datagen object/instance, ImageDatagenerator class of Keras will augment/transform the image
                                   shear_range = 0.2,      #Feature scaling is Utterly IMP in Neural network , each pixel of image is in range 0-255 , so scalling b/w 0 & 1 by dividing each pixel by 255
                                   zoom_range = 0.2,       #Applying Shear, zoom and horizontal flip
                                   horizontal_flip = True)

#Now importing the dataset & applying these transformation features to it and creating batches
training_set = train_datagen.flow_from_directory(   #flow_from_directory is the method of ImageDataGenerator to connect the transformation features to training data
        'dataset/training_set',                     #Directory/location/path of our training data
        target_size = (64, 64),                     #Final size of the Images fed to Convolutional neural network = 64 by 64
        batch_size = 32,                            #Creating batches of size 32 within train data
        class_mode = 'binary'                       #O/p is binary or value , as classification have binary o/p = Cat/Dog
)

"""### Preprocessing the Test set"""

#We're not gonna apply transformation features to test set , just apply the feature scaling on the test set, keep them original
#Just like fit_transform on train set & only transform on test set

test_datagen = ImageDataGenerator(rescale = 1./255)
test_set = test_datagen.flow_from_directory('dataset/test_set',
                                            target_size = (64, 64),
                                            batch_size = 32,
                                            class_mode = 'binary')

"""## Part 2 - Building the CNN

### Initialising the CNN
"""

#Before feeding the I/p to ANN , we've to create 3 layer - Convolution  MaxPooling and flattening layer to perform their tasks,
#After that Flattened layer is connected to Ann i/p layer for classification

#Implementation of CNN is same as the ANN Just the before convolution is applied to the dataset
cnn = tf.keras.models.Sequential()

#cnn is created as object/instance of Sequential class

"""### Step 1 - Convolution"""

#Applying the convolution on images matrix to create the convolved feature map
#ConV2D IS the function of layers class to perform convolution on our image dataset
#Parameters given to ConV2D are no of filters/feature detectors to be applied to image,
#kernel_size = size of feature detector = 3 by 3 matrix
#input_shape = size of image matrix on which convolution is to be performed , train data=64 by 64 , 3 = RGB Colored images , 1 = b&w image
#Relu activation function applied to break linearity in the image, also used in hidden layers of ANN

cnn.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu', input_shape=[64, 64, 3]))

"""### Step 2 - Pooling"""

#Now applying & adding pooling layer on our convolved layer
#When applying Maxpooling on our feature map/ convolve map , pool matrix of size 2 by 2 is applied & maximum of each square matrix
#of ConvolvedMap is extracted & pool feature map is created - see slides
#Pool size of 2 by 2 matrix is used to apply Maxpooling

cnn.add(tf.keras.layers.MaxPool2D(pool_size = 2, strides = 2 ))     #MaxPooling applied on Convolved layer

#Another parameter Stride = no of pixels shift when pooling each 2 by 2 square matrix of convolved map = 2 pixels

"""### Adding a second convolutional layer"""

#Similarly 2nd hidden layer added & convolution & pooling performed in these layers too.
cnn.add(tf.keras.layers.Conv2D(filters = 32, kernel_size = 3, activation = 'relu'))
cnn.add(tf.keras.layers.MaxPool2D(pool_size = 2, strides = 2))

"""### Step 3 - Flattening"""

#Converting the pooled feature map to vector of one column

cnn.add(tf.keras.layers.Flatten())
#Flatten class will take all pooled matrix & apply flattening to it.

"""### Step 4 - Full Connection"""

#Now the flattened layer matrix containing vector of features is to be fed to ANN as input layer
#Now first layer of Ann is added/implemented = i/p layer will be fully connected to Flattened layer
#Here we're dealing with Computer Vision more complex problem than data mining
#128 No of neurons hidden layers are initialised so as to obtain better accuracy

cnn.add(tf.keras.layers.Dense(units = 128, activation = 'relu', ))

"""### Step 5 - Output Layer"""

#Softamx as o/p layer activation function is used to range the probabilities of o/p b/w 0 & 1

cnn.add(tf.keras.layers.Dense(units = 1, activation = 'sigmoid'))

#Here convolutional neural network is build , pretty smart model with eyes to predict the image as Dog/Cat

"""## Part 3 - Training the CNN

### Compiling the CNN
"""

#Now compliling CNN with parameters to follow while classifying within hidden layers

cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'] )

"""### Training the CNN on the Training set and evaluating it on the Test set"""

cnn.fit(x = training_set, validation_data = test_set, epochs = 25)
                         #fixed attribute name for test_set is validation_data

#As no of epochs , Increasing the number of epochs means that the model will be trained for longer as dataset used is very large.
#This can lead to better performance on the training set, but it also increases the risk of overfitting.
#Overfitting occurs when the model learns the training data too well and does not generalize well to new data.

#To mitigate overfitting, you can use techniques like early stopping, regularization, or data augmentation.

#Each batch has 32 images , total 8000 images = 8000/32 = 250 batches would be trained for 25 times/epochs

"""## Part 4 - Making a single prediction"""

import numpy as np    #numpy required to deal with array created from image for prediction

#Predict method only allows the same i/p as training set for prediction, so we have to perform these steps

from keras.preprocessing import image  #To load single image from directory, submodule 'image' of preprocessing module from keras library is used
test_image = image.load_img('dataset/single_prediction/a.jpg', target_size = (64,64)) #To import image from directory , class 'load_img'of image submodule is used, Also trained images were 64 by 64, so test_img should be of same dimension
test_image = image.img_to_array(test_image) #As input of predict method is 2D array, so we need to convert the image to array using 'img_to_array' class of image sub module
test_image = np.expand_dims(test_image, axis = 0) #Expand the shape of an array, As batches of images were given for training, another dimension for batches made in training phase, so we need to add that dimension as predict method take exact same i/p as train set, (np.expand_dims(array,axis))

#Now predict method can be called
result = cnn.predict(test_image)

#Now obtained o/p is numerical = 0/1=cat/dog, so to make it categorical , we need to obtain for respective class
training_set.class_indices  #we've got the right indices value representing each class at o/p layer for both classes

if result[0][0] == 1:      #Then obtained indices compared to o/p and categorical value obtained
  prediction = 'Dog'
else:
  prediction = 'Cat'

  #result[0][0] - accessing the 0th batch & 0th element of that batch of result conatining final prediction.

print(prediction)

#Now implement this code on Jupyter notebook - is a platform used for deployment of ML codes having several python IDES like jupyter notebook
#and spyder, provides environment for ml models and projects to deploy, have librarys to work with ML & DL Models
#Install Anaconda Software on your Mac
#Install Librarys as Tensorflow and keras on your system using command terminal.