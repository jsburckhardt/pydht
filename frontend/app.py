from flask import Flask
from flask import render_template
import sqlite3
from datetime import time

conn = sqlite3.connect('../sensorsData.db', check_same_thread=False)
curs = conn.cursor()


app = Flask(__name__)

def maxRowsTable():
    for row in curs.execute("select COUNT(temp) from  DHT_data"):
        maxNumberRows = row[0]
    return maxNumberRows

# initialize global variables
global numSamples
numSamples = maxRowsTable()
if (numSamples > 101):
    numSamples = 100

def getLastData():
    for row in curs.execute("SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT 1"):
        time = str(row[0])
        temp = row[1]
        hum = row[2]
    # conn.close()
    return time, temp, hum    

def getHistData(numSamples):
    curs.execute(
        "SELECT * FROM DHT_data ORDER BY timestamp DESC LIMIT "+str(numSamples))
    data = curs.fetchall()
    dates = []
    temps = []
    hums = []
    for row in reversed(data):
        dates.append(row[0])
        temps.append(row[1])
        hums.append(row[2])
    return dates, temps, hums

# main route
@app.route("/")
def index():
    time, temp, hum = getLastData()
    times, temps, hums = getHistData(100)
    templateData = {
        'time'		: time,
        'temp'		: temp,
        'hum'			: hum,
        'numSamples'	: numSamples,
        'values_temp': temps,
        'labels_temp': times,
        'legend_temp': 'Temperature',
        'values_hum': hums,
        'labels_hum': times,
        'legend_hum': 'Humidity'
    }
    return render_template('index.html', **templateData)

# @app.route("/chart_temp")
# def chart_temp():
#     legend = 'Temperature'
#     times, temps, hums = getHistData(100)
#     # labels = ["January", "February", "March",
#     #           "April", "May", "June", "July", "August"]
#     # values = [10, 9, 8, 7, 6, 4, 7, 8]
#     return render_template('chart.html', values=temps, labels=times, legend=legend)

# @app.route("/chart_hum")
# def chart_hum():
#     legend = 'Humidity'
#     times, temps, hums = getHistData(100)
#     # labels = ["January", "February", "March",
#     #           "April", "May", "June", "July", "August"]
#     # values = [10, 9, 8, 7, 6, 4, 7, 8]
#     return render_template('chart.html', values=hums, labels=times, legend=legend)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)
