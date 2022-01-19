# importing the module
import json
import os
import argparse
import time
import threading
import requests
import utils as ut
from datetime import datetime,timezone

class SessionLogger():
    def __init__(self):
        self.timer_flag  = False
        self.timer       = threading.Thread(target=self.fun_timer, name="Logging") #,daemon="True")
        self.current_s   = ut.LOG_FILE
        self.weather_url = 'http://wttr.in/?format=j1'

    def fun_timer(self):
        while self.timer_flag:
            data     = self.get_current()
            new_read = self.get_readings()
            new_data = data["session"]["readings"].append(new_read)
            self.update_file(json.dumps(data))
            print("logged: {}".format(new_read))
            time.sleep(1800)
            #time.sleep(60)

    def start(self):
        self.timer_flag   = True
        self.timer.start()

    def stop(self):
        self.timer_flag   = False
        self.timer.join()
    
    def update_file(self, data):
        #print(data)
        with open(self.current_s, 'w') as f:
            f.write(data)

    def get_current(self):
        data = {}
        with open(self.current_s, 'r') as f:
            data = json.load(f)
            #print(data)
        return data

    def get_readings(self):
        now      = ut.get_now()
        wort     = ut.ds18b20_to_display()
        env      = ut.dht22_to_display()
        cpu      = ut.get_cpu_temp()
        weather  = self.get_weather_info()
        new_read = { "date": now,
                "env": { "celsius": env["celsius"], "fahrenheit": env["fahrenheit"] },
                "wort": { "celsius": wort["celsius"], "fahrenheit": wort["fahrenheit"] },
                "cpu": { "celsius": round(cpu,2), "fahrenheit": round(ut.c_to_f(cpu),2) },
                "humidity": env["humidity"],
                "current_conditions": weather['current_condition'][0],
                "nearest_area": weather['nearest_area'][0]
                }
        return new_read

    def get_weather_info(self):
        weather_info = json.loads(requests.get(self.weather_url).text)
        #print(weather_info)
        return weather_info


if __name__ == "__main__":
    session = SessionLogger()
    parser = argparse.ArgumentParser()
    parser.add_argument("action")
    args = parser.parse_args()
    if args.action == "start":
        print("Starting logging session")
        session.start()
    elif args.action == "stop":
        print("Stoping session")
        session.stop()

