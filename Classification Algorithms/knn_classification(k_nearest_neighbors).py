# -*- coding: utf-8 -*-
"""KNN- Classification(K_Nearest_Neighbors).ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/12uMU8VbsqLpzxQ5U6P7k3sBxyID4JRuO

# K-Nearest Neighbors (K-NN)

Simplest Classification Algorithm - major code similar to logistic regression , only training model is different

In KNN , K nearest neighbour ,

Choose No of K = no of neighbours

You have to calculate the Euclidean distance b/w point and it's nearest neighbour.

Among these k neigbours calculate no of datapoints in each category.

Assign the new datapoint to the category have most neighbours.

Model is ready


Two points P1(x1,y1) p2(x2,y2) , Euclidean's distance - ((x2-x1)ˆ2+(y2-y1)ˆ2)ˆ1/2

Calculate euclidean distance b/w 5 neighbours and the category with neighbours having less distance , the new data point will be classified
into that category.

## Importing the libraries
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

"""## Importing the dataset"""

dataset = pd.read_csv('Social_Network_Ads.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25, random_state = 0)

print(X_train)

print(y_train)

print(X_test)

print(y_test)

"""## Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)

print(X_test)

"""## Training the K-NN model on the Training set"""

#KNeighborsClassifier class of neighbors module of scikitlearn library is used.
#n_neighbors is the no of neighbors from which you want to find distance between , n=3,5 or wwhat ever
#IMP*** - Metric is which method to find the distance b/w point and neighbor - "for euclidean minkowski keyword is used"
#p =1 means manhattan distance , p= 2 means euclidean distance

from sklearn.neighbors import KNeighborsClassifier
classifier = KNeighborsClassifier(n_neighbors=5 ,metric = 'minkowski' , p =2)
classifier.fit(X_train ,y_train)          # training done here

"""## Predicting a new result"""

print(classifier.predict(sc.transform([[30,87000]])))

"""## Predicting the Test set results"""

y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1), y_test.reshape(len(y_test),1)),1))

#very few incorrect predictions compared to logistic regression-high accuracy

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

"""## Visualising the Training set results"""

from matplotlib.colors import ListedColormap
X_set, y_set = sc.inverse_transform(X_train), y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 1),
                     np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 1))
plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('salmon', 'dodgerblue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('salmon', 'dodgerblue'))(i), label = j)
plt.title('K-NN (Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

#very compute intensive plot - takes too much time
#Decison boundary isn't linear & created by calculating distance b/w the nearest neighbors and then classifying them to hat category &
#decison boundary is created.

"""## Visualising the Test set results"""

from matplotlib.colors import ListedColormap
X_set, y_set = sc.inverse_transform(X_test), y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 10, stop = X_set[:, 0].max() + 10, step = 1),
                     np.arange(start = X_set[:, 1].min() - 1000, stop = X_set[:, 1].max() + 1000, step = 1))
plt.contourf(X1, X2, classifier.predict(sc.transform(np.array([X1.ravel(), X2.ravel()]).T)).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('salmon', 'dodgerblue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1], c = ListedColormap(('salmon', 'dodgerblue'))(i), label = j)
plt.title('K-NN (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()