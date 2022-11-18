import time
import machine
import json
from settings import ssid, password, ip_address, sensor_correction
from phew import connect_to_wifi, logging, server, ntp
from dht import DHT11

connect_to_wifi(ssid, password, ip_address)
timestamp = ntp.fetch(synch_with_rtc=True, timeout=10)

onboard_led = machine.Pin("LED", machine.Pin.OUT)
sensor = DHT11(machine.Pin(28, machine.Pin.OUT, machine.Pin.PULL_DOWN))

onboard_led.value(0)

logging.truncate(5)

def getTimeString():
    now = time.localtime()
    return str(now[3]) + ":" + str(now[4])

def getDateString():
    now = time.localtime()
    return str(now[0]) + "-" + str(now[1]) + "-" + str(now[2])

def getJsonResponse():
    humidity = 0
    tempC = 0
    tempF = 0
    corrected_tempC = 0
    corrected_tempF = 0
    try:
        humidity = sensor.humidity
        tempC = sensor.temperature
        tempF = (tempC * 9/5) + 32
        
        corrected_tempC = tempC + sensor_correction
        corrected_tempF = (corrected_tempC * 9/5) + 32
    except Exception as e:
        print(e)
        logging.error(e)
    
    data = {
        "tempC": tempC,
        "tempF": tempF,
        "humidity": humidity,
        "timestamp": getDateString() + " " + getTimeString() + " UTC",
        "sensor_correction_C": sensor_correction,
        "corrected_tempC": corrected_tempC,
        "corrected_tempF": int(corrected_tempF), 
    }

    return json.dumps(data)

@server.route("/json", methods=["GET"])
def jsonHandler(request):
    return getJsonResponse(), 200, "application/json"

@server.route("/log", methods=["GET"])
def logHandler(request):
    text_file = open("log.txt", "r")
    data = text_file.read()
    text_file.close()
    return data, 200, "application/json"

@server.route("/dashboard", methods=["GET"])
def logHandler(request):
    html_file = open("html/dashboard.html", "r")
    response = html_file.read()
    html_file.close()
    return response, 200, "text/html"

@server.route("/help", methods=["GET"])
def logHandler(request):
    response = """
        <!doctype html>
        <html>

        <head>
            <title>Help Page</title>
        </head>

        <body>
            <h3>Endpoints</h3>
            <div>/json - json output for temp and humidity</div>
            <div>/log - output system log</div>  
        </body>

        </html>
    """
    return response, 200, "text/html"

@server.catchall()
def catchall(request):
    return "Not found see /help for valid endpoints", 404

# Start Server
server.run()
