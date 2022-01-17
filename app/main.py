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
    def pretty_date(date):
        return ut.pretty_date(date)
    return dict(convert_fahrenheit=convert_fahrenheit,get_now=get_now,pretty_date=pretty_date)

@app.route("/")
def main():
    cpu         = ut.get_cpu_temp()
    environment = ut.dht22_to_display()
    probe       = ut.ds18b20_to_display()
    logs        = ut.get_session_history()
    return render_template("index.html",environment=environment,probe=probe,cpu=cpu,session_log=logs)
    #video_streaming       = threading.Thread(target=ut.start_camera_streaming_service, name="Thread1",daemon="True")
    #video_streaming.start()
    

if __name__ == "__main__":
    app.run(host='0.0.0.0')
