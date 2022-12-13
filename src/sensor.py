from dht import DHT11
from settings import sensor_correction, node_name
import machine, json, utils

hardware_sensor = DHT11(machine.Pin(28, machine.Pin.OUT, machine.Pin.PULL_DOWN))

class Sensor:
    def __init__(self):
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
        try:
            hardware_sensor.measure()
            humidity = hardware_sensor.humidity
            tempC = hardware_sensor.temperature
            corrected_tempC = tempC + sensor_correction
            corrected_tempF = int((corrected_tempC * 9/5) + 32)

            self.data["humidity"] = humidity
            self.data["tempF"] = corrected_tempF
            self.data["time"] = utils.getDateTimeString()

            if corrected_tempF > self.data["high_temp"]:
                self.data["high_temp"] =  corrected_tempF

            if corrected_tempF < self.data["low_temp"]:
                self.data["low_temp"] =  corrected_tempF
            
        except Exception as e:
            print("readSensor error:", e)

    def resetHighLow(self):
        self.data["high_temp"] = self.data["tempF"]
        self.data["low_temp"] = self.data["tempF"]

    def getJsonResponse(self):
        return json.dumps(self.data)

    def getHistory(self):
        return json.dumps(self.tempHistory)

    def saveToHistory(self):
        # Every 15 minutes for 24 hours minus 1 to avoid overlap.
        DATA_POINTS_TO_KEEP = 95

        data = {
            "temperature": self.data["tempF"], 
            "timestamp": self.data["time"],
            "humidity": self.data["humidity"]
        }
        if len(self.tempHistory) > DATA_POINTS_TO_KEEP:
            # Remove oldest entry in the list
            self.tempHistory.pop(0)
        
        # Add newest entry to end of list
        self.tempHistory.append(data)


# Export a single instance of the class
sensor = Sensor()
