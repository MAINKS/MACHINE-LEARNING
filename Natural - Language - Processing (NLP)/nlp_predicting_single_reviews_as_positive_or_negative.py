# -*- coding: utf-8 -*-
"""NLP - Predicting Single Reviews as Positive or Negative,ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_LYcnKbceoLSH4QrixIPJoOv7LwoFsu4

# Natural Language Processing

In this module we'll implement to train a machine to understand the text & predict the outcomes for the these texts or new test dataset.

Simple & basic : We've text as in Restaurant review , will train our machine to predict whether the review is positive or not.

Sort of classification model to predict the binary outcome whether a review is positive (1) or not (0)

Using naive bayes classification , we'll implement this Text recognition model

TSV - Tab separated value

CSV - comma separated value

## Importing the libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

"""## Importing the dataset"""

dataset = pd.read_csv('Restaurant_Reviews.tsv', delimiter = '\t', quoting = 3)

# delimiter = '\t'used to indicate we have tsv file reading via pd.read_csv command
# our dataset have double quotes , for model to not classify them as text they can create sparsing error, So quoting = 3 means to ignore them.

"""## Cleaning the texts"""

#Simplify the text- remove punctuations, letters in lowercase, apply stemming as, Very clean dataset required to eleviate the learning process.
#Stopwords , punctuations , lowercase

import re   #IMP  - library used to simplify the reviews - clean/stemming the datset
import nltk  #IMP - library essential to download the ensemble of stop words - stop words are words not required to include in our dataset after cleaning
#Stop Words are not helpful to predict - doesn't invest in result generation,  the result  , EX : the , or , as , them etc

nltk.download('stopwords')   #downloading irrevelant stop words list from nltk library.
from nltk.corpus import stopwords  #after downloading , importing those stopwords using "CORPUS" module of nltk library
from nltk.stem.porter import PorterStemmer #For stemming dataset , Class PorterStemmer from stem.porter module/submodule is imported from nltk library
#stemming means only including root of word that indicates what this word means
#Ex : someone said 'I loved this restaurant' , stemming will stem the loved word to love = positive review
#If we don't apply stemming we'll have two columns then love & loved = redundancy, so it's essential as bag of words conatin sparse matrix of
# each columns = diff words & that's what stemming is all about to reduce the trouble & have clean dataset.

corpus =[]  #list gonna have all cleaned dataset reviews , each time we clean a row is then appended here.

for i in range(0,1000):   #Going row wise to each 1000 review,  now gonna clean each and every review row-wise of our dataset.
  review = re.sub('[^a-zA-Z]', ' ' , dataset['Review'][i])  #re.sub('[not^ a-z & A-Z and everything else]' , ' replace with ', which dataset)
  #review variable created - sub fxn will be used to convert/replace all punctuations to spaces (_)  (Only letters left)
  review = review.lower()    #Got review with no punctuations & now uppercase letters converted to lowercase here.
  review = review.split()   #all words are spearated from one another in review cleaned dataset

  #Now removing the stopwords downloaded above -    Stemming part
  ps = PorterStemmer()    #Object of porterstemmer class created
  all_stopwords = stopwords.words('english')  # contains all stopwords
  all_stopwords.remove('not')  #as not keyword is in stopwords which is required to predict negative comments.
  review = [ps.stem(word) for word in review if not word in set (all_stopwords)]#Perform loop on review list , stop words not to be included in dataset
  #calling stem fxn from porterstemmer class & applying on each word on review datasst , without punctuation , stopwords excluded

  review = ' '.join(review) #Python's " JOIN " Function will join all words back , ' '.join(data) space given, else will create a one word of all
  corpus.append(review) #Adding cleaned data (review) back to list corpus

  print(corpus)

"""## Creating the Bag of Words model"""

#Now all the cleaned datatset would be added to the Bag of words and each word = column in vector list of bag of words
#Tokenization : taking all the words from tsv file & transforming to the Columns for each words is Tokenization
#Each row contains each review, with each columns contains each word of each review.

from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features = 1500) #Total no of ci\olumns = 1566 . taking 1500 to remove all these irrelevant words from list.
#for bag of words implementation , scikitlearn library ⏩ feature_extraction module ⏩ text submodule ⏩ CounVectorizer class is used.
#As still there are more words that don't contribute to any o/p = steve , rick, may , texture & others, so Fixed sparse vector matrix will be
#created to have frequently used words and removing these irrelevant words.

X = cv.fit_transform(corpus).toarray()
#Fit / Trainining data / fetch data intoo model form corpus, & transforimg it to the vector with each column = word & saved to array of data.
y = dataset.iloc[:,-1].values # dependent variable with last column is created.

len(X[0])  #Length of / no of words in each row

"""## Splitting the dataset into the Training set and Test set"""

from sklearn.model_selection import train_test_split
X_train , X_test , y_train , y_test = train_test_split(X,y , test_size = 0.2 , random_state = 0)

"""## Training the Naive Bayes model on the Training set"""

from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train , y_train)

"""## Predicting the Test set results"""

y_pred = classifier.predict(X_test)
print(np.concatenate((y_pred.reshape(len(y_pred),1),y_test.reshape(len(y_test),1)),1))

"""## Making the Confusion Matrix"""

from sklearn.metrics import confusion_matrix , accuracy_score
cm = confusion_matrix(y_pred, y_test)
print(cm)
accuracy_score(y_pred, y_test)

#In this way model was able to study and learn the Language and provide results
#Use other classification algos too so as to get the better accuracy

"""# Using our NLP Model We'll be predicting whether a Single Review is classified as Positive or Negative Review

# Positive review

Use our model to predict if the following review:

"I love this restaurant so much"

is positive or negative.

Solution: We just repeat the same text preprocessing process we did before, but this time with a single review.
"""

new_review = 'I love this restaurant so much'
new_review = re.sub('[^a-zA-Z]', ' ', new_review)
new_review = new_review.lower()
new_review = new_review.split()
ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')
new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
new_review = ' '.join(new_review)
new_corpus = [new_review]
new_X_test = cv.transform(new_corpus).toarray()
new_y_pred = classifier.predict(new_X_test)
print(new_y_pred)


print(new_review)

#The review was correctly predicted as positive by our model.

"""# Negative review

"I hate this restaurant so much"

is positive or negative.


"""

new_review = 'I hate this retaurant so much'
new_review = re.sub('[^a-zA-Z]', ' ', new_review)
new_review = new_review.lower()
new_review = new_review.split()
ps = PorterStemmer()
all_stopwords = stopwords.words('english')
all_stopwords.remove('not')
new_review = [ps.stem(word) for word in new_review if not word in set(all_stopwords)]
new_review = ' '.join(new_review)
new_corpus = [new_review]
new_X_test = cv.transform(new_corpus).toarray()
new_y_pred = classifier.predict(new_X_test)
print(new_y_pred)

print(new_review)

#The review was correctly predicted as negative by our model.