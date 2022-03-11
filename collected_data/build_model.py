'''
Author: Ahmed Badra
Version: 1.0.0
Description: python script for training, evaluating and saving the model in the server's directory
'''

# import required Packages
from sklearn.model_selection import train_test_split as tts
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
from sklearn.metrics import accuracy_score
from xgboost import XGBClassifier
import pandas as pd
import pickle
import os

# reading the data
df = pd.read_csv('train.csv')
X = df.drop(columns = ['location'])
y = df['location']

# splitting the data
X_train, X_val, y_train, y_val = tts(X, y, test_size=0.2)

clf = {}

# Fitting RandomForest Classifier to the training set
clf["RandomForest"] = RandomForestClassifier(n_estimators = 200, random_state=0, max_depth = 7, min_samples_split = 20, max_leaf_nodes = 7)
clf["RandomForest"].fit(X_train, y_train)

#Fitting XGB Classifier to the training set  
clf["XGBoost"] = XGBClassifier(eta=0.1, gamma=0.1)
clf["XGBoost"].fit(X_train, y_train)

print("RESULTS:\n================================\n")

# print the results for each classifier we added to the clf dictionary
for key in clf.keys():
    print(f"{key} Classifier:\n")
    y_pred = clf[key].predict(X_val)
    print("validation accuracy: ", accuracy_score(y_pred, y_val).round(3))
    y_pred = clf[key].predict(X_train)
    print("training accuracy: ", accuracy_score(y_pred, y_train).round(3))

    print("-------------------------------------\n")

# choose the directory to save the models to
save_dir = input("Enter the relative path to store these models:")
os.chdir(save_dir)

# loop over all the classifiers and save each one with it's name
for key in clf.keys():
    filename = os.path.abspath(os.getcwd()) + '\\' + f"{key}.sav"
    with open(filename, 'wb') as files:
        pickle.dump(clf[key], files)

print("saved successfully.")