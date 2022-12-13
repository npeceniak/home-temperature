import network, ubinascii, machine, time, usocket, struct, gc, settings
gc.threshold(50000)

def connect_to_wifi():
    ssid = settings.ssid
    password = settings.password
    ip_address = settings.ip_address
    timeout_seconds=30

    print("Connecting to wifi network:", ssid)

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.config(pm = 0xa11140) # Disable power-save mode
    wlan.connect(ssid, password)
    if ip_address != None:
        # Values represent IP address, netmask, gateway, DNS.
        # gateway may need to be updated based on network config
        wlan.ifconfig((ip_address, '255.255.255.0', '192.168.5.1', '8.8.8.8'))
    else:
        print("No Static Ip set. Using DHCP")

    
    mac = ubinascii.hexlify(network.WLAN().config('mac'),':').decode()
    print("Mac Address:", mac)

    start = time.ticks_ms()
    while (time.ticks_ms() - start) < (timeout_seconds * 1000):
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        time.sleep(0.1)

    if wlan.status() != 3:
        print("Failed to connect")
        return None

    print("Ip address: ", wlan.ifconfig()[0])

    return wlan.ifconfig()[0]

def syncClock(synch_with_rtc=True, timeout=10):
    ntp_host = "pool.ntp.org"

    timestamp = None
    try:
        query = bytearray(48)
        query[0] = 0x1b
        address = usocket.getaddrinfo(ntp_host, 123)[0][-1]
        socket = usocket.socket(usocket.AF_INET, usocket.SOCK_DGRAM)
        socket.settimeout(timeout)
        socket.sendto(query, address)
        data = socket.recv(48)
        socket.close()
        local_epoch = 2208988800 # UTC
        mst_offset = 25200 # Set to MST UTC-7 7 hours in seconds
        timestamp = struct.unpack("!I", data[40:44])[0] - local_epoch - mst_offset
        timestamp = time.gmtime(timestamp)
    except Exception as e:
        print("Sync Time Error: ", e)
        return None

    # if requested set the machines RTC to the fetched timestamp
    if synch_with_rtc:
        machine.RTC().datetime((
            timestamp[0], timestamp[1], timestamp[2], timestamp[6], 
            timestamp[3], timestamp[4], timestamp[5], 1))
        print("System Time Set: ", getDateTimeString())


    return timestamp


def getDateTimeString():
  dt = machine.RTC().datetime()
  return "{0:04d}-{1:02d}-{2:02d} {4:02d}:{5:02d}".format(*dt)