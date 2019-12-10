from flask import Flask
from flask import jsonify
from flask import g
import sqlite3
from flask_cors import CORS

DATABASE = 'pythonsqlite.db'

app = Flask(__name__)
CORS(app)


# Method to connect to the database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


# Method to query the database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


# Method to close the connection to database
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


# GET ENDPOINT to return data based on date from, date to and parameter name
@app.route('/data/date-from/<dateFrom>/date-to/<dateTo>/param/<param>')
def data(param=None, dateFrom=None, dateTo=None):
    data = []
    for i in query_db('select * from data where Datum >= ? and Datum <= ?', [dateFrom, dateTo]):
        data.append({"date": i['Datum'], "param": i[param], "stationNumber": i['StationNumber']})
    return jsonify(data)\


# GET ENDPOINT to return data based on date from, date to, parameter name and station number
@app.route('/data/date-from/<dateFrom>/date-to/<dateTo>/param/<param>/sn/<sn>')
def dataWithSn(sn=None, param=None, dateFrom=None, dateTo=None):
    data = []
    for i in query_db('select * from data where Datum >= ? and Datum <= ? and StationNumber = ?', [dateFrom, dateTo, sn]):
        data.append({"date": i['Datum'], "param": i[param], "stationNumber": i['StationNumber']})
    return jsonify(data)


# GET ENDPOINT to return data about stations
@app.route('/geodata')
def geodata():
    data = []
    for i in query_db('select * from stations'):
        data.append({"stationNumber": i['StationNumber'], "latitude": i['Latitude'], "longitude": i['Longitude']})
    return jsonify(data)


if __name__ == '__main__':
    # run application
    app.run(host='0.0.0.0', debug=True)
