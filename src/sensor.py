from dht import DHT11
from settings import sensor_correction, node_name, api_hostname
import machine, json, utils, urequests

hardware_sensor = DHT11(machine.Pin(28, machine.Pin.OUT, machine.Pin.PULL_DOWN))

class Sensor:
    def sendReading(self):
        try:
            hardware_sensor.measure()
            tempC = hardware_sensor.temperature
            corrected_tempC = tempC + sensor_correction
            corrected_tempF = int((corrected_tempC * 9/5) + 32)

            formatted_data = {
                "location": node_name,
                "humidity": hardware_sensor.humidity,
                "temp_f": corrected_tempF,
                "temp_c": corrected_tempC,
                "timestamp": utils.getDateTimeString()
            }

            post_endpoint = 'http://' + api_hostname
            post_headers = {'content-type': 'application/json'}
            post_data = json.dumps(formatted_data)

            try:
                resp = urequests.post(post_endpoint, headers=post_headers, data=post_data)
                resp.close()
            except Exception as e:
                print("Post exception:", e)
            
        except Exception as e:
            print("readSensor error:", e)

# Export a single instance of the class
sensor = Sensor()
