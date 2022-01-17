import os
import json
import Adafruit_DHT
from datetime import datetime,timezone
from tzlocal import get_localzone


DEVICE_FOLDER = "/sys/bus/w1/devices/"
DEVICE_SUFFIX = "/temperature"
WAIT_INTERVAL = 0.2

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24

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


def get_ds18b20_temperature(device=None):
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
    else:
        return False


def get_now():
    return datetime.now(timezone.utc).isoformat()

def get_temp_style(temp):
    output = int(c_to_f(temp)) if isinstance(temp,float) else 0
    if output % 2 == 0:
        return output
    else:
        return output + 1

def dht22_to_display():
    output = {}
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        output["celsius"]    = round(temperature,2)
        output["fahrenheit"] = round(c_to_f(temperature),2)
        output["humidity"]   = round(humidity,2)
        output["valid"]      = True
    else:
        output["celsius"]    = "N/A"
        output["fahrenheit"] = "N/A"
        output["humidity"]   = "N/A"
        output["valid"]      = False
    output["style"]          = get_temp_style(temperature)
    return output

def ds18b20_to_display():
    output = {}
    temperature = get_ds18b20_temperature()
    if temperature:
        output["celsius"]    = round(temperature,2)
        output["fahrenheit"] = round(c_to_f(temperature),2)
        output["valid"]      = True
    else:
        output["celsius"]    = "N/A"
        output["fahrenheit"] = "N/A"
        output["valid"]      = False
    output["style"]          = get_temp_style(temperature)
    return output

def get_session_history():
    log = "/home/pi/sessions/current.json"
    if os.path.exists(log):
        data = {}
        with open(log,'r') as f:
            data = json.load(f)
            env_avg  = list_average(data,"env")
            wort_avg = list_average(data,"wort")
            data["env_avg"]  = env_avg
            data["wort_avg"] = wort_avg
        return data
    else:
        return False

def list_average(data,what):
    readings_amount = 0 #len(data['session']["readings"])
    readings_sum = 0
    for deg in data['session']["readings"]:
        if isinstance(deg[what]["fahrenheit"],float):
            readings_sum += deg[what]["fahrenheit"]
            readings_amount += 1
    if readings_amount > 0:
        avg = round(readings_sum / readings_amount,2)
    else:
        avg = 0
    return avg


def pretty_date(date):
    easy_format = "%m/%d/%Y %H:%M %Z"
    utc = datetime.fromisoformat(date)
    local_time = utc.astimezone(get_localzone())
    return local_time.strftime(easy_format)

def start_camera_streaming_service():
    global foo
    print("starting streaming")
    foo = __import__('app.picamera_stream')
    print("streaming started")


