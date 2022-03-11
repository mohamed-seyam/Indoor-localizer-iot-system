'''
Author          : Ahmed Badra
version         : 1.0.0
Functionality   : this script concatenate the csv data files in it's current directory to one large csv file.
                    preprocess that file, prepare it for the machine learning model, split it to train and test and
                    write them out in the same directory as csv files 
'''

# import required Packages
import pandas as pd 
import numpy as np 
import os
from sklearn.model_selection import train_test_split as tts

# setup your working directory (the relative directory containing the raw data)
raw_dir = input("Enter the relative Directory of the raw data files:")
os.chdir('./raw_data')

# dictionary of the mapped locations (the labels of the collected data to integers)
locations_id = {
   '3201 upper left':16,
   '3201 upper right':1,
   '3201 lower left':2,
   '3201 lower right':3,
   'HW 11':4,
   'HW 12':5,
   'HW 21':6,
   'HW 22':7,
   'HW 23':8,
   'HW 31':9,
   'HW 32':10,
   'HW 33':11,
   'EL 11':12,
   'EL 12':13,
   'TAMER 11':14,
   'TA 11':15,
}

# list of csv files 
csv_files = os.listdir()

# filter out the other files in the directory except csv
for file in csv_files:
    if not file.endswith(".csv"):
        csv_files.remove(file)
print("found these files in the directory: ", csv_files)


print("reading the files to dataframes...")

# list of dataframes to be filled 
dataframes = []

# read all the csv files and add them to dataframes list
for idx, csv_file in enumerate(csv_files):
    # read the csv
    dataframe = pd.read_csv(os.path.abspath(os.getcwd()) + '\\' + csv_file)
    # convert all strength values to integers
    dataframe.iloc[:, :-1] = dataframe.iloc[:, :-1].astype('int64')
    # get the location of this csv file
    location = dataframe.loc[0, 'location']
    # print out this location
    print(f"reading the file of {location} location to an dataframe...")
    # convert the location column values to the corresponding id of that location
    dataframe['location'] = locations_id[location]
    # add this dataframe to the list
    dataframes.append(dataframe)
    # print the status of reading current file
    print("read this file successfully!")

print("read out all the csv files into dataframes successfully")
print("concatenating all the dataframes into one dataframe...")

# concatenate all the dataframes readed from all the locations stores in each csv file
df = pd.concat(dataframes, axis = 'index', join = 'outer', ignore_index = True)

print("concatenated successfully!")

print("preprocessing the data...")
# remove the location column and put it at the end of the columns as it's our target variable
df = df[[column for column in df.columns if column not in ['location']] + ['location']]

# fill the nulls with -100 indicating very weak strength
df.fillna(-100, inplace=True)

print("preprocessing done!")

print("these are the Networks found in the entire dataset:")
print(df.columns.unique())

# input a list of the networks you will be using in your training and evaluation
selected_networks = input("Enter the list of Networks you want in your dataset (seperated by comma):").split(',')
for idx, network in enumerate(selected_networks):
    selected_networks[idx] = selected_networks[idx].strip(" \'")

df = df[selected_networks + ['location']]

print("splitting the data...")

# generate X, y for splitting usage
y = df.drop(columns = ['location'])
X = df

# splitting the indecies into training and testing
test_size = float(input("Enter the selected test_size: "))
X_train, X_test, y_train, y_test = tts(X.index, y, test_size=test_size)

# getting the entire df of the training and testing samples
df_train = df.iloc[X_train]
df_test = df.iloc[X_test]

print("done splitting the data")

print("saving the train and test csv file in the current directory...")

# switch the operating directory to the current file's directory
os.chdir("./")

# delete the old train and test files
try:
    pass
    os.remove("./train.csv")
    os.remove("./test.csv")
except:
    pass

# store the new train and test files
df_train.to_csv('train.csv', encoding='utf-8', index=False)
df_test.to_csv('test.csv', encoding='utf-8', index=False)

print("saved successfully.")