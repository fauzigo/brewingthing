from flask import Flask
from flask import Flask, render_template
import threading
#from app.utils import get_cpu_temp, c_to_f, start_camera_streaming_service, get_probe_temperature
#import app.utils as ut
import utils as ut

app = Flask(__name__)

@app.context_processor
def utility_processor():
    def convert_fahrenheit(celsius):
        return ut.c_to_f(celsius)
    def get_now():
        return ut.get_now()
    return dict(convert_fahrenheit=convert_fahrenheit,get_now=get_now)

@app.route("/")
def main():
    #humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    #immersed_temp         = ut.get_immersed_temperature()
    cpu         = ut.get_cpu_temp()
    environment = ut.dht22_to_display()
    probe       = ut.ds18b20_to_display()
    return render_template("index.html",environment=environment,probe=probe,cpu=cpu)
    #print(immersed_temp)
    #video_streaming       = threading.Thread(target=ut.start_camera_streaming_service, name="Thread1",daemon="True")
    #video_streaming.start()
    """
    if humidity is not None and temperature is not None and immersed_temp and cpu_temp:
        #print("Temp={0:0.1f}*C  Humidity={1:0.1f}%".format(temperature, humidity))
        return render_template("index.html",temperature=temperature,humd=humidity,cpu_temp=cpu_temp,wort_temp=immersed_temp)
    else:
        return render_template("index.html",temperature=temperature,humd=humidity,cpu_temp=cpu_temp,wort_temp=immersed_temp)
        print("Failed to retrieve data from a sensor")
        #return("Nothing to show")
    return render_template("index.html",temperature=temperature,humd=humidity,cpu_temp=cpu_temp,wort_temp=immersed_temp)
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0')
