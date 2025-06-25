I'm using virtual distance sensor and camera sensor (counterfit) to do this assignment
# Set up
- Install requirements:
```
pip install -r requirements.txt
```
# How to use
- Active virtual environment
```
source .venv/bin/activate
```
- Run counterfit and set up sensors
    
    + In terminal (on local device)
    ```
    counterfit
    ```
    + Must to create distance sensor first (use the default I<sup>2</sup>C address)
    + Create a camera sensor with the name "sensor_1"

- Set up adafruitIO
    + Create or log in an adafruit account
    + create 3 feeds with these names (you can use other names, changes the name of feeds in app.py with the real name):
        + distance
        + fruit-result
        + led-control
    + Create and set up a dashboard (optional)

- Set up and run app.py
    + Fill your adafruitIO USERNAME and KEY 
    + Open another terminal 
    + Active venv
    + Change the path to the location of app.py
    ```
    cd "path/to/app.py"
    ```
    + Run
    ```
    python app.py
    ```
