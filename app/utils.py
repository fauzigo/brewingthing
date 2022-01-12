import os
from datetime import datetime,timezone


DEVICE_FOLDER = "/sys/bus/w1/devices/"
DEVICE_SUFFIX = "/temperature"
WAIT_INTERVAL = 0.2

CPU_THERMAL = '/sys/class/thermal/thermal_zone0/temp'

def get_cpu_temp():
    """
    Obtains the current value of the CPU temperature.
    :returns: Current value of the CPU temperature if successful, zero value otherwise.
    :rtype: float
    """
    # Initialize the result.
    result = 0.0
    # The first line in this file holds the CPU temperature as an integer times 1000.
    # Read the first line and remove the newline character at the end of the string.
    if os.path.isfile(CPU_THERMAL):
        with open(CPU_THERMAL) as f:
            line = f.readline().strip()
        # Test if the string is an integer as expected.
        if line.isdigit():
            # Convert the string with the CPU temperature to a float in degrees Celsius.
            result = float(line) / 1000
    # Give the result back to the caller.
    return result


def c_to_f(celsius):
    fahrenheit = celsius * 1.8 + 32
    return fahrenheit


def guess_temperature_sensor():
    """
    Try guessing the location of the installed temperature sensor
    """
    devices = os.listdir(DEVICE_FOLDER)
    devices = [device for device in devices if device.startswith('28-')]
    if devices:
        # print "Found", len(devices), "devices which maybe temperature sensors."
        return DEVICE_FOLDER + devices[0] + DEVICE_SUFFIX
    else:
        return False
        #sys.exit("Sorry, no temperature sensors found")


def get_immersed_temperature(device=None):
    """
    Get a raw temperature reading from the temperature sensor
    """
    if device is None:
        device = guess_temperature_sensor()

    if not device:
        return False

    raw_reading = None
    with open(device, 'r') as sensor:
        #print(sensor.read())
        #raw_reading = sensor.readlines()
        raw_reading = sensor.read()
    if raw_reading != -1:
        #print(raw_reading)
        temperature = float(raw_reading) / 1000.0
    return temperature


def get_now():
    return datetime.now(timezone.utc).isoformat()

def get_temp_style(temp):
    output = c_to_f(temp) if isinstance(temp,int) else 0
    return output

def start_camera_streaming_service():
    global foo
    print("starting streaming")
    foo = __import__('app.picamera_stream')
    print("streaming started")


