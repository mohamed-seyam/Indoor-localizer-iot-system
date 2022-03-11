'''
Author: Ahmed Badra
Version: 1.0.0
Description: test the service API using the selected json data file
'''

# importing the requests library
import requests
import json

json_dir = input("Enter the json data file path: ")

URL = "https://python-server-model.herokuapp.com/addlocation"

file = open(json_dir)

json_obj = json.load(file)

for item in json_obj:
    # send the data through a POST http request
    response = requests.post(url=URL, json=item)
    # extracting response text
    print("The response is: %s"%response.text)