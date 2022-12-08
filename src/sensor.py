from dht import DHT11
from settings import sensor_correction, node_name
import machine
import json
import time
from phew import logging

sensor = DHT11(machine.Pin(28, machine.Pin.OUT, machine.Pin.PULL_DOWN))

class Sensor:
    def __init__(self):
        logging.info("Initialize Sensor")
        self.data = {
                "name": node_name,
                "humidity": 0,
                "tempF": 0,
                "time": "",
                "high_temp": 0,
                "low_temp": 200
            }
        self.tempHistory = []
        self.readSensor()

    def readSensor(self):
        logging.info("readSensor Called")
        now = time.localtime()
        try:
            sensor.measure()
            humidity = sensor.humidity
            tempC = sensor.temperature
            corrected_tempC = tempC + sensor_correction
            corrected_tempF = int((corrected_tempC * 9/5) + 32)

            self.data["humidity"] = humidity
            self.data["tempF"] = corrected_tempF
            self.data["time"] = str(now[0]) + "-" + str(now[1]) + "-" + str(now[2]) + " " + str(now[3]) + ":" + str(now[4])

            if corrected_tempF > self.data["high_temp"]:
                self.data["high_temp"] =  corrected_tempF

            if corrected_tempF < self.data["low_temp"]:
                self.data["low_temp"] =  corrected_tempF
            
        except Exception as e:
            logging.error(e)

    def resetHighLow(self):
        logging.info("Resetting High and Low values for today.")
        self.data["high_temp"] = self.data["tempF"]
        self.data["low_temp"] = self.data["tempF"]

    def getJsonResponse(self):
        return json.dumps(self.data)

    def getHistory(self):
        return json.dumps(self.tempHistory)

    def saveToHistory(self, timestamp=None):
        # Every 10 minutes for 24 hours.
        DATA_POINTS_TO_KEEP = 144

        data = {
            "temperature": self.data["tempF"], 
            "timestamp": timestamp or self.data["time"],
            "humidity": self.data["humidity"]
        }
        logging.info("Saving ", data)
        if len(self.tempHistory) > DATA_POINTS_TO_KEEP:
            # Remove oldest entry in the list
            self.tempHistory.pop(0)
        
        # Add newest entry to end of list
        self.tempHistory.append(data)