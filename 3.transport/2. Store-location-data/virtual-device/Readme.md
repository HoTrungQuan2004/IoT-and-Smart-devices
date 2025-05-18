# Overview
I am using adafruitIO and CounterFit instead of Azure store and Azure IoT hub

## Set up environment
- Use the package manager [pip](https://pip.pypa.io/en/stable/) to install necessary packages:
```bash
pip install adafruit-io
pip install counterfit
pip install counterfit-shims-serial
pip install eventlet
pip install flask
pip install flask-socketio
pip install paho-mqtt
pip install pynmea2
pip install setuptools
```

## Virtual environment
- Create: (skip if there is already one)
```bash
python3 -m venv .venv
```
- Active
```bash
source .venv/bin/activate
```

## Run CounterFit
- in .venv terminal, run:
```bash
counterfit
```

- Open CounterFit in browser
- Add UART GPS
- Use source NMEA
- Add a NMEA, for example: $GPGGA,123519,3723.2475,N,12158.3416,W,1,08,0.9,545.4,M,46.9,M,,*59
- Click "repeat" (if not counterfit will only send NMEA 1 time)
- Click "Set"

## Run app.py
- Active .venv in another terminal
```bash
source .venv/bin/activate
```
- Move to parent folder of app.py
```bash
cd "path-to-parent-folder"
```
- In this terminal, run:
```bash
python3 app.py
```


- Then app.py will send the data of counterfit to adafruitIO