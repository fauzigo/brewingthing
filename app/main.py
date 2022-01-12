from flask import Flask
from flask import Flask, render_template
import Adafruit_DHT
import threading
#from app.utils import get_cpu_temp, c_to_f, start_camera_streaming_service, get_probe_temperature
#import app.utils as ut
import utils as ut

app = Flask(__name__)
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 24

@app.context_processor
def utility_processor():
    def convert_fahrenheit(celsius):
        return ut.c_to_f(celsius)
    def get_now():
        return ut.get_now()
    return dict(convert_fahrenheit=convert_fahrenheit,get_now=get_now)

@app.route("/")
def main():
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    cpu_temp              = ut.get_cpu_temp()
    immersed_temp         = ut.get_immersed_temperature()
    #print(immersed_temp)
    #video_streaming       = threading.Thread(target=ut.start_camera_streaming_service, name="Thread1",daemon="True")
    #video_streaming.start()
    if humidity is not None and temperature is not None and immersed_temp and cpu_temp:
        #print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        #celsius    = round(temperature,2)
        #humidity   = round(humidity,2)
        #cpu_temp   = round(cpu_temp,2)
        return render_template("index.html",temperature=temperature,humd=humidity,cpu_temp=cpu_temp,wort_temp=immersed_temp)
    else:
        return render_template("index.html",temperature=temperature,humd=humidity,cpu_temp=cpu_temp,wort_temp=immersed_temp)
        print("Failed to retrieve data from humidity sensor")
        return("Nothing to show")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
