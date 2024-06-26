# -*- coding: utf-8 -*-
"""Data_Preprocessing_Tool.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1tO4Oi4u8x6o6zTA3OQx9nFyvO1HqZRnC

# Data Preprocessing Tools

Fit & transform working

**fit(df):**

Calculates the mean and variance for each feature in the dataset df

Mean for Feature1: (1 + 2 + 3 + 4 + 5) / 5 = 3

Mean for Feature2: (10 + 20 + 30 + 40 + 50) / 5 = 30

Variance for Feature1: variance calculation

Variance for Feature2: variance calculation

Stores these values internally in the StandardScaler object.

output
Mean (fit): [ 3. 30.]

Variance (fit): [ 2. 200.]


**transform(df):**

Uses the mean and variance stored during fit to standardize the data.

For each value in the dataset:

Transforms each value by subtracting the mean and dividing by the standard deviation.

For example, the first value in Feature1: (1 - 3) / sqrt(2) = -1.414 (approx)

Output

Transformed DataFrame (transform):
[[-1.41421356 -1.41421356]
 [-0.70710678 -0.70710678]
 [ 0.          0.        ]
 [ 0.70710678  0.70710678]
 [ 1.41421356  1.41421356]]

**fit_transform(df):**

Performs both the fit and transform steps in one call.

First, it calculates and stores the mean and variance.

Then, it transforms the dataset using these stored values.
"""

#Librarys are the symobol of modules containing functions and classes used to perform operations and actions. ex scikit learn contains all Ml required classes that we can use to create object of.

#Numpy - will allow us to work with arrays as Ml model requires array as input.

#Matplotlib - to plot graphs and charts , .pyplot is a module

#Pandas - allow us to import datasets & create matrix of features & dependent vector variable.

#Data slicing is done [1:9,8:10]
#Scikit learn is the library highly used in ml & have a module "model selection"used for Data preprocessing.

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
#!pip install scikit-learn

"""## Importing the dataset"""

dataset = pd.read_csv('Data.csv')
X = dataset.iloc[: , :-1].values
y = dataset.iloc[: , -1].values

print(X)

print(y)

"""# Take care of missing data"""

#Using average of all salarys , you can get the missing values in the columns.

#Scikit learn is library used to do this task. Class "simpleimputer" will be used.

#Imputer is created object of class "simpleimputer"

#Providing only numeric values(1st & 2nd col) to imputer using fit keyword.

#All rows and only columns with numeric data from X Matrix containing independent variables.
#Transform is used to update the values in the matrix.

from sklearn.impute import SimpleImputer  #importing simpleimputer from scikit library
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')  # creating object of class simpleimputer indicating task to perform & method
imputer.fit(X[:,1:3])   # accessing missing values from matrix
X[:,1:3]=imputer.transform(X[:,1:3])  # Updating missing values
print(X)

"""## Encoding categorical data

### Encoding the Independent Variable
"""

# Converting categorical data into numerical data ,Country column containing (germany,france,spain) will be converted to numerical data.
# Germany france spain will be categorized individually
# Dependent variable (purchase) will be (Yes-1 , No - 0).
# One columntransfer class of compose module from scikit-learn library is used.
# Second class Onehotencoding from preprocessing module of scikit library is used to achieve this conversion.
# from sklearn.compose import ColumnTransformer
#      library  module        class name

# a new object (ct) of columntransformer class is created
#Matrix x is then transformed and fitted , stored in object ct as an array.

# MOST IMPORTANT:
#ColumnTransformer with Onehotencoder will be applied when column has variables as (germany,france,spain)
#LabelEncoder will be applied when column has variables as (Yes,No)

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
ct=ColumnTransformer(transformers=[('encoder', OneHotEncoder(),[0])] , remainder='passthrough')
#Object   class       details        encoder    encoding class  columns to transform.    remainder req to mention
X = np.array(ct.fit_transform(X))    #O/p saved in array , so array conversion is required
print(X)


#O/p - 10100 france 01001 spain 01010 germany are encoded in in binary.

"""#Encoding Dependent Variable"""

#Importing class labelencoder from preprocessing module of sklearn library
#create an object name le for class label encoder
#applying fit & transform on Matrix y using object le created from labelencoder class to encode it to numerical value

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
le.fit(y)
y=le.transform(y)
       #or
y=LabelEncoder().fit_transform(y) #for ease
print(y)

"""# Splitting the dataset into the Training set and Test set"""

#IMP #Feature scaling is always applied after splitting data into training & test dataset as if
#done before , variation in the dataset will be observed due to mean standardisation that is
#not required in the test dataset used for model training - To prevent information leakage - as test set is supposed to be something new.

#Module "Model selection" with a defined class "Train_test_split" is used for spliiting dataset.
#4 matrices two for train & two for test dataset with each of dependent & independent variable.

from sklearn.model_selection import train_test_split
X_train , X_test , y_train , y_test = train_test_split(X , y , test_size=0.2 , random_state=1)

# X & y matrices of train/test data  class name  Input as complete matrix X & y  data split size = 80/20  randomly splitting

print(X_train)
print("")
print(X_test)
print("")
print(y_train)
print("")
print(y_test)

"""## Feature Scaling"""

# Feature scaling allows us to put all our data features on the same scale.
#To avoid some features dominating other features. To have all th value of features in the same range.
#Standardisation & normalisation
#Normalisation is preferred when we have normal features in most of the distrubiution
#Standardisation works in majorly all the conditions and is more preferred.   X_stand = X - mean(x)/StandardDeviation(X)
#Feature scaling is not done on test set , performed over train set & then transformed onto test set.

#StandardScaler class for standardisation from preprocessing module of scikitlearn library is imported.
#StandardScaler class will automatically calculate mean and steandard deviation of X matrix & standardise the features of matrix and scaling is done.


#Most Asked ques by DataScience Community : Do we have to apply feature scaling on dummy variables in a matrix of features
#Answer : No , as dummy variables are already in the same scale range as other variables.
#Only apply Standardisation feature scaling to your numerical values only - Age & salary , don't apply on Country as it's dummy variable. Slicing of columns will be done.
#On X_train & test matrix it is applied , not on y matrix containing categorical data.


from sklearn.preprocessing import StandardScaler
sc=StandardScaler()   #object created
X_train[: , 3:]=sc.fit_transform(X_train[: , 3:])
X_test[:,3:]=sc.transform(X_test[:,3:])  #same scale used on both test and train matrix of X(Numerical data)
#All Rows & 3rd col onwards.    fit will calc the mean & StDeviation & transform will put into formula & calculate.
print(X_train)
print("\n")
print(X_test)


#Scaling of features age & salary done b/w range -2 & 2.
#Will help optimise training of ML model.