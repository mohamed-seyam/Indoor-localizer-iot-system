'''
Author: Ahmed Badra
Version: 1.0.0
Description: this python script convert the csv data file to the json format and save it in the user selected directory  
'''

import json, csv

# get the user's paths 
filepath = input("Enter the csv file path: ")
outputpath = input("Enter the json output file path: ")

# function to convert from csv to json
def make_json(filepath, outputpath):
    # open the csv file
    with open(filepath, encoding='utf-8') as csvfile:
        # read it as a csvreader object
        csvreader = csv.DictReader(csvfile)

        json_items = []
        #loop over the rows of the object
        for row in csvreader:
            # convert the row into a dictionary and append it to the json_items list
            json_items.append(dict(row))

        # open the json output file
        with open(outputpath + '/testing_json.json', 'w', encoding='utf-8') as jsonfile:
            # convert the list of Dicts into a json string then write it into the opened json file
            jsonfile.write(json.dumps(json_items, indent=4))

# Driver Code
make_json(filepath, outputpath)