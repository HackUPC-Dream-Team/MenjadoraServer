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
    
    c.execute("DELETE FROM feed WHERE 1")

    # DATA VALIDATION
    for action in actions:
        hour = action['Hour']
        min = action['Min']
        amount = action['Amount']

        time = hour * 3600 + min * 60
        c.execute("INSERT INTO feed VALUES (?, ?)", [amount, time])
        db.commit()
        
    return jsonify(status="OK")

@app.route("/capture", methods=['GET'])
def capture():
    print "CAPTURING!"
    time.sleep(10)
    return jsonify(status="OK")

@app.route("/schedule", methods=['GET'])
def hello():
    dades = get_current_feed_schedule()
    dades = { 'actions': dades }
    return jsonify(dades)

if __name__ == "__main__":
    app.run('10.4.180.158', debug=True)