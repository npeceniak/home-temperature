import time, gc, utils, server, routes, uasyncio
from sensor import sensor

gc.threshold(50000)

utils.connect_to_wifi()
utils.syncClock()

async def main():
    print("Starting Web Server")
    uasyncio.create_task(uasyncio.start_server(server._handle_request, '0.0.0.0', 80))

    # This loop should run once every minute
    while True:
        READ_SENSOR_INTERVAL_MINUTE = 5
        SAVE_TO_HISTORY_INTERVAL_MINUTE = 15

        now = time.localtime()
        hour = now[3]
        minute = now[4]

        # Read sensor every 5 minutes.
        if minute % READ_SENSOR_INTERVAL_MINUTE == 0:
            sensor.readSensor()

        # Save every 10 minutes.
        if minute % SAVE_TO_HISTORY_INTERVAL_MINUTE == 0:
            sensor.saveToHistory()

        if hour == 0 and minute == 0:
            sensor.resetHighLow()

        await uasyncio.sleep(60) #Seconds

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()