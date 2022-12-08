import time
import machine
import uasyncio
from settings import ssid, password, ip_address, sensor_correction
from phew import connect_to_wifi, logging, server, ntp
from sensor import Sensor

connect_to_wifi(ssid, password, ip_address)
ntp.fetch(synch_with_rtc=True, timeout=10)

onboard_led = machine.Pin("LED", machine.Pin.OUT)

onboard_led.value(0)

logging.truncate(5)

sensor = Sensor()

def getTimeString():
    now = time.localtime()
    return str(now[3]) + ":" + str(now[4])

def getDateString():
    now = time.localtime()
    return str(now[0]) + "-" + str(now[1]) + "-" + str(now[2])

@server.route("/json", methods=["GET"])
def jsonHandler(request):
    return sensor.getJsonResponse(), 200, "application/json"

@server.route("/history", methods=["GET"])
def jsonHandler(request):
    return sensor.getHistory(), 200, "application/json"

@server.route("/log", methods=["GET"])
def logHandler(request):
    text_file = open("log.txt", "r")
    data = text_file.read()
    text_file.close()
    return data, 200, "application/json"

@server.route("/dashboard", methods=["GET"])
def logHandler(request):
    html_file = open("web/html/dashboard.html", "r")
    response = html_file.read()
    html_file.close()
    return response, 200, "text/html"

@server.route("/chart", methods=["GET"])
def logHandler(request):
    html_file = open("web/html/chart.html", "r")
    response = html_file.read()
    html_file.close()
    return response, 200, "text/html"

@server.catchall()
def catchall(request):
    path = "web" + request.path
    fileType = ""
    
    if path[-4] == ".css":
        fileType = "text/css"
    elif path[-3] == ".js":
        fileType = "text/javascript"
    elif path[-5] == ".html":
        fileType = "text/html"
    
    try:
        file = open(path, "r")
        response = file.read()
        file.close()
        return response, 200, fileType
    except:
        logging.error("Request to ", path, " not found")
        return "Not found", 404


async def main():
    logging.info("Starting Web Server")
    uasyncio.create_task(uasyncio.start_server(server._handle_request, '0.0.0.0', 80))

    # This loop should run once every minute
    while True:
        READ_SENSOR_INTERVAL_MINUTE = 5
        SAVE_TO_HISTORY_INTERVAL_MINUTE = 10
        now = time.localtime()

        hour = now[3]
        minute = now[4]

        # Read sensor every 5 minutes.
        if minute % READ_SENSOR_INTERVAL_MINUTE == 0:
            logging.info("Reading Sensor")
            sensor.readSensor()

        # Save every 10 minutes.
        if minute % SAVE_TO_HISTORY_INTERVAL_MINUTE == 0:
            logging.info("Saving to history....")
            # TODO: Pass a timestamp to this function.
            sensor.saveToHistory()

        if hour == 0 and minute == 0:
            sensor.resetHighLow()

        await uasyncio.sleep(60) #Seconds

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()