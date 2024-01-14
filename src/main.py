import time, gc, utils, uasyncio
from sensor import sensor

gc.threshold(50000)

utils.connect_to_wifi()
utils.syncClock()

async def main():
    # This loop should run once every minute
    while True:
        READ_SENSOR_INTERVAL_MINUTE = 5

        now = time.localtime()
        minute = now[4]

        # Read sensor every 5 minutes.
        if minute % READ_SENSOR_INTERVAL_MINUTE == 0:
            sensor.sendReading()

        await uasyncio.sleep(60) #Seconds

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
