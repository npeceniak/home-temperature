from dht import DHT11
from settings import sensor_correction
import machine
import json
import time
from phew import logging

sensor = DHT11(machine.Pin(28, machine.Pin.OUT, machine.Pin.PULL_DOWN))

class Sensor:
    def __init__(self):
        logging.info("Initialize Sensor")
        self.data = {
                "tempC": None,
                "tempF": None,
                "humidity": None,
                "corrected_tempC": None,
                "corrected_tempF": None,
                "time": None,
                "high_temp": None,
                "low_temp": None
            }
        self.tempHistory = []

    def readSensor(self):
        logging.info("readSensor Called")
        now = time.localtime()
        try:
            sensor.measure()
            humidity = sensor.humidity
            tempC = sensor.temperature
            tempF = (tempC * 9/5) + 32
            corrected_tempC = tempC + sensor_correction
            corrected_tempF = (corrected_tempC * 9/5) + 32

            self.data = {
                "tempC": tempC,
                "tempF": tempF,
                "humidity": humidity,
                "corrected_tempC": corrected_tempC,
                "corrected_tempF": int(corrected_tempF),
                "time": str(now[0]) + "-" + str(now[1]) + "-" + str(now[2]) + " " + str(now[3]) + ":" + str(now[4]),
                "high_temp": 0,
                "low_temp": 0
            }

        except Exception as e:
            logging.error(e)

    def getJsonResponse(self):
        return json.dumps(self.data)

    def getHistory(self):
        return json.dumps(self.tempHistory)

    def saveToHistory(self, timestamp):
        data = {
            "temperature": self.data["corrected_tempF"], 
            "timestamp": timestamp or self.data["time"],
            "humidity": self.data["humidity"]
        }
        logging.info("Saving ", data)
        if len(self.tempHistory) > 100:
            # Remove oldest entry in the list
            self.tempHistory.pop(0)
        
        # Add newest entry to end of list
        self.tempHistory.append(data)