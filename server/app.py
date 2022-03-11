from flask import Flask, request, jsonify, render_template
import sqlite3
import pickle
import numpy as np

#--------------------------------#
#    update section              #
#--------------------------------#
db_file = 'db/database_new.db'
model = pickle.load(open('XGBoost.sav', 'rb'))
features = ['El-lab', 'El-modarag', 'Redmi', 'youssef', 'Farouk', 'Ramadan', 'badra22', 'STUDBME2', 'ARC3', 'CMP_LAB2', 'CMP_LAB3', 'STUDBME1', 'CMP_LAB1', 'CMP_LAB4', 'CMP-lab1', 'ARC1', 'BMEStudentLab3', 'STUDBME3']

mobile_map = {
      16 :(-0.8, 7.8),
      1 : (0.2, 7.8),
      2 : (0.8, 9.0),
      3 : (-0.2, 9.0),
      4 : (0.6, 8.8),
      5 : (0.6, 7.6),
      6 : (2.0, 6.6),
      7 : (0.6, 6.6),
      8  :(-0.5, 6.6),
      9 : (0.6, 5.0),
      10 :(0.6, 3.0),
      11 :(0.6, 0.8),
      12 :(2.2, 3.8),
      13: (1.2, 3.8),
      14: (1.6, 2.0),
      15: (1.5, 5.8)
}

website_map ={
4 :
            {'x_val': -7.7 , 'y_val': 274},
5 :
            {'x_val': -8.4 , 'y_val': 201},
3 :
            {'x_val': -63.7 , 'y_val': 138.4},
2 :
            {'x_val': -74.8 , 'y_val': 135.65},
1 :
            {'x_val': -62.7 , 'y_val': 73.7},
16 :
            {'x_val': -75.68 , 'y_val': 73.7},
6 :
            {'x_val': 68.6 , 'y_val': 86.5},
7 :
            {'x_val': -9.8 , 'y_val': 85},
8 :
            {'x_val': -75.3 , 'y_val': 87.2},
15 :
            {'x_val': 43 , 'y_val': 6.3},
12 :
            {'x_val': 69 , 'y_val': -71},
13 :
            {'x_val': 36.6 , 'y_val': -71},
9 :
            {'x_val': -8.4 , 'y_val': 6.3},
10 :
            {'x_val': -8.4 , 'y_val': -71},
11 :
            {'x_val': -8.4 , 'y_val': -223.6},
14:
            {'x_val': 42 , 'y_val': -223.6}    
}


def predict(model, data):
    input = []
    for feature in features:
        try:
            input.append(float(data[feature]))
        except:
            input.append(-100)

    val = model.predict(np.array(input).reshape(1, -1))[0]
    print(type(val))
    return val


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file,check_same_thread=False)
    except Error as e:
        print(e)

    return conn

def create_table(conn):
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS Position (location INTEGER NOT NULL)')
    message = "table created successfully"
    print(message)
    
    return message

def select_values(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Position ORDER BY rowid DESC limit 1")
    data = cur.fetchone()
    return data

def select_replay_values(conn):
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT * FROM Position ORDER BY rowid DESC limit 5")
    data = cur.fetchall()
    return data                                                


def push_values(conn, location):
    location = float(location)
    cur = conn.cursor()
    cur.execute('insert into Position (location) values (?)',(location,))
    conn.commit()
    message = "pussed successfully"
    
    return message

conn = create_connection(db_file)
create_table(conn)


app = Flask(__name__)
# from flask_cors import CORS
# CORS(app)

@app.route('/')
def index(): 
    return render_template("home.html")


@app.route('/addlocation', methods=['GET', 'POST', 'DELETE', 'PUT'])                                                                                                    
def add():
    data = request.get_json()
    location = int(predict(model, data))
    result = push_values(conn,location)
    loc = select_values(conn)
    loc = loc[0]
    return jsonify(x_val_azoz=float(mobile_map[loc][0]),
                   y_val_azoz=float(mobile_map[loc][1]),
                   x_val_seyam=float(website_map[loc]['x_val']),
                   y_val_seyam=float(website_map[loc]['y_val']))



@app.route('/getdata')

def get_data():
    loc = select_values(conn)
    loc = loc[0]
    return jsonify(x_val_azoz=float(mobile_map[loc][0]),
                   y_val_azoz=float(mobile_map[loc][1]),
                   x_val_seyam=float(website_map[loc]['x_val']),
                   y_val_seyam=float(website_map[loc]['y_val']))


@app.route('/getreplaydata')
def get_replay_data():

    locations = select_replay_values(conn)

    json_output = "["
    for idx, loc in enumerate(locations):
        loc = loc[0]
        json_output += "{" + f'''"x_val_azoz": {float(mobile_map[loc][0])},''' + f'''"y_val_azoz": {float(mobile_map[loc][1])},''' + f'''"x_val_seyam": {float(website_map[loc]['x_val'])},''' + f'''"y_val_seyam": {float(website_map[loc]['y_val'])}''' + "}"
        if idx < (len(locations)-1):
            json_output += ","

    return json_output + "]"



if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000, debug = True)