from dht import DHT22
from settings import sensor_correction, node_name, api_hostname, sensor_type
import machine, json, utils, urequests

dht11 = sensor_type == "dht11"

hardware_sensor = DHT22(machine.Pin(28, machine.Pin.OUT, machine.Pin.PULL_DOWN),dht11=dht11)
class Sensor:
    def sendReading(self):
        try:
            tempC, humidity = hardware_sensor.read()
            corrected_tempC = tempC + sensor_correction
            corrected_tempF = round((corrected_tempC * 9/5) + 32)

            formatted_data = {
                "humidity": round(humidity),
                "temp_f": corrected_tempF,
                "timestamp": utils.getDateTimeString()
            }

            # print(formatted_data)

            post_endpoint = 'http://' + api_hostname + '/temperature/' + node_name

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
