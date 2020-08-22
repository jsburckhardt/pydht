import time
import sqlite3
import Adafruit_DHT
dbname='/home/pi/pysensor/sensorsData.db'
# sampleFreq = 1*60 # time in seconds ==> Sample each 1 min
# get data from DHT sensor
def get_dht_data():	
	dht22_sensor = Adafruit_DHT.DHT22
	dht_pin = 22
	hum, temp = Adafruit_DHT.read_retry(dht22_sensor, dht_pin)
	if hum is not None and temp is not None:
		hum = round(hum)
		temp = round(temp, 1)
	return temp, hum
# log sensor data on database
def log_data (temp, hum):
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("INSERT INTO DHT_data values(datetime('now'), (?), (?))", (temp, hum))
	conn.commit()
	conn.close()
	print(f"Inserting temp: {temp} and hum: {hum}")
# main function
def main():
	print("Started")
	temp, hum = get_dht_data()
	log_data (temp, hum)
	print("Finished")
# ------------ Execute program 
main()