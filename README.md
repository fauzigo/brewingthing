# brewingthing

Thing to check on brewing sessions temperatures

Comprised by a raspberry pi with a DHT22 and a DS18B20 sensors connected to the raspberry's GPIO board. We intend to check on temperatures related to brewing sessions. Temperature of the wort, and temperature and humidity of the environment, and show up the information in a browser through Flask.

Additionally, the application collect external weather information through wttr.in. Currently, nothing external is shown up in the browser, but might at some point.

## How to

Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Copy the unit file, this would enable the service and let you access information of the brewing session.

```bash
cd brewingthing
cp unit_files/brewingthing.service /etc/systemd/system/
sudo systemctl enable brewingthing --now
```

Now you should be able to access the raspberry pi's IP address or domain name over port 8080 (ex. http://brewingthing:8080 or http://192.168.0.100:8080)

## Data log

You can add a new service to record readings every half an hour into a json file at `/home/pi/sessions/current.json`. If you do, make sure there is an initial `current.json` file in the location mentioned, otherwise the service will fail.

```bash
cd brewingthing
cp unit_files/brewinglogging.service /etc/systemd/system/
sudo systemctl enable brewinglogging --now
```

Check on `session_example.json` for an example of the log file.

Additionally, if logging is enabled, you can access `/ext` for and extended report (ex. http://brewingthing:8080/ext or http://192.168.0.100:8080/ext)
NOTE: Right now only show outside's temperature, thanks to wttr.in

Update: 
* 2022-01-28: wttr.in has a limitation of 1MM calls overall, so it might just fail if others using the service. openweather can be used instead if you are willing to use their API and create a key for it. Check on the `brewing_example.json` for an example of the configuration file that can be used to access openweather API. Also uncoment the environment variable on the unit file for `brewinglogging.service` if you want to use the feature. For more information regarding openweather: https://openweathermap.org/current



##  Hardware Implementation

![temperatureControl_bb](temperatureControl_bb.svg)
