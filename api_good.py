from flask import Flask, jsonify, request
import time
import sqlite3
app = Flask(__name__)

print "ayy"

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

db = sqlite3.connect('database.db', check_same_thread=False)
db.row_factory = dict_factory
c = db.cursor()

def isTimeFormat(i):
    try:
        time.strptime(i, '%H:%M')
        return True
    except ValueError:
        return False

def get_current_feed_schedule():
    c.execute("SELECT * FROM feed")
    return c.fetchall()

def isDigit(i):
    return isinstance(i, (int, long))

@app.route("/schedule", methods=['POST'])
def psch():
    data = request.get_json()
    actions = data['actions']
    
    # DATA VALIDATION
    for action in actions:
        if(not isDigit(action['amount']) and not isTimeFormat(action['time'])):
            return jsonify(status="Error")

        if(not isDigit(action['time'])):
            if(isTimeFormat(action['time'])):
                struct = time.strptime(action['time'], "%H:%M")
                l = list(struct)
                l[0] += 70 
                struct = time.struct_time(l)
                print struct
                action['time'] = time.mktime(time.strptime(action['time'], "%H:%M"))

        if(action['time'] > 86400 or action['time'] < 0):
            return jsonify(status="Error")

    c.execute("DELETE FROM feed WHERE 1")
    for action in actions:
        c.execute("INSERT INTO feed VALUES (?, ?)", [action['amount'], action['time']])
    return jsonify(status="OK")

@app.route("/schedule", methods=['GET'])
def hello():
    dades = get_current_feed_schedule()
    dades = { 'actions': dades }
    return jsonify(hola="miglosli")

if __name__ == "__main__":
    app.run('10.4.180.158', debug=True)