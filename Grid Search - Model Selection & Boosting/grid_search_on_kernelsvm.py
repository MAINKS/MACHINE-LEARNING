# -*- coding: utf-8 -*-
"""Grid_Search_on_KernelSVM.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/11_Lc5q4GToycy7zn8HFSYMjU5Dm8WB--

# Grid Search
"""

#Model selection technique used to find Highest accuracy model as well as Hyperparameters = gamma & parameters = linear,rbf etc
#Hyperparameters are the parameters applied other than parameters on which model is trained.
#Providing grid search on parameters to find the one with best accuracy obtained on our model.

"""## Importing the libraries"""

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

"""## Feature Scaling"""

from sklearn.preprocessing import StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

"""## Training the Kernel SVM model on the Training set"""

from sklearn.svm import SVC
classifier = SVC(kernel = 'rbf', random_state = 0)
classifier.fit(X_train, y_train)

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix, accuracy_score
y_pred = classifier.predict(X_test)
cm = confusion_matrix(y_test, y_pred)
print(cm)
accuracy_score(y_test, y_pred)

"""## Applying k-Fold Cross Validation"""

from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
print("Accuracy: {:.2f} %".format(accuracies.mean()*100))
print("Standard Deviation: {:.2f} %".format(accuracies.std()*100))

"""## Applying Grid Search to find the best model and the best parameters"""

#Implemented Kfold above just to compare best_accuracy obtained & compare,

#We'll be using Linear and rbf kernel hyperparameters to apply grid search onto them
#Also gamma is the coeffiecient in sigmoid and rbf kernel parameters, We'll use 0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9 as values of gamma
#C is the regularisation parameter in KernelSVC , The strength of the regularization is inversely proportional to C.
#We'll use the 0.25,0,5,0.75,1 as value of C, to test the accuracy on them, As C increases regularisation decreases.

#model_selection module have GridSearchCV class for implementing gridsearch for model on various paramaters
#Create two dictionaries to give two parameters to consider for grid search in key value pair, one hyperparameter = gamma
#object of GridSearchCV class , takes i/p parameters as estimator, parameters , scoring
#Each of these combinations of hyperparameters will be evaluated by K-FoldCV, not on single set of data, so cv as parameter is provided

#So what grid search will do is perform K fold using all parameters given to it sequentially & calculate accuracies for them & provide the
#best model and parameter of all.

from sklearn.model_selection import GridSearchCV
parameters = [{'C': [0.25, 0.5, 0.75, 1], 'kernel': ['linear']},
              {'C': [0.25, 0.5, 0.75, 1], 'kernel': ['rbf'], 'gamma' : [0.1,0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]}]

grid_search = GridSearchCV(estimator = classifier,
                           param_grid = parameters,
                           scoring = 'accuracy',
                           cv = 10,
                           n_jobs = -1) #For long processes, command n_jobs used to use all cpu processors (-1) for execution , as for each 0.25-1 for linear then rbf then gamma with 0.1-0.9 is highly resource consuming

grid_search.fit(X_train, y_train)   #perform training on training set, using given parameters & hyperparamters & methods & obtain best of all.
best_accuracy = grid_search.best_score_     #Grid_searchCV has attribute best_score_ to fetch best accuracy obtained via grid search
best_parameters = grid_search.best_params_  #Grid_searchCV has attribute best_params_ to fetch best parameter obtained via grid search


print("Best Accuracy: {:.2f} %".format(best_accuracy*100))  #.2f - till 2 decimal points, *100 - convert to % format
print("Best Parameters:", best_parameters)

#Best accuracy obtained in GridSearchCV > cross_val_score , slight increase
#Best Parameters obtained is rbf , radial based function when applied using gamma function of 0.6 and regularisation parameter = 0.5

"""## Visualising the Training set results"""

from matplotlib.colors import ListedColormap
X_set, y_set = X_train, y_train
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('salmon', 'dodgerblue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('salmon', 'dodgerblue'))(i), label = j)
plt.title('Kernel SVM (Training set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()

"""## Visualising the Test set results"""

from matplotlib.colors import ListedColormap
X_set, y_set = X_test, y_test
X1, X2 = np.meshgrid(np.arange(start = X_set[:, 0].min() - 1, stop = X_set[:, 0].max() + 1, step = 0.01),
                     np.arange(start = X_set[:, 1].min() - 1, stop = X_set[:, 1].max() + 1, step = 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha = 0.75, cmap = ListedColormap(('salmon', 'dodgerblue')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())
for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set == j, 0], X_set[y_set == j, 1],
                c = ListedColormap(('salmon', 'dodgerblue'))(i), label = j)
plt.title('Kernel SVM (Test set)')
plt.xlabel('Age')
plt.ylabel('Estimated Salary')
plt.legend()
plt.show()