These assignments are using CounterFit as virtual sensors instead of real sensors
### Setup:
in root path (/workspaces/IoT-and-Smart-devices), run in terminal to create and active virtual environment
```bash
python -m venv .venv #can skip if already have one
```
```bash
source .venv/bin/activate
```
Install requirements:
```bash
pip install -r requirements.txt
```
To activate CounterFit, run in terminal:
```bash
counterfit
```

# Notes:
If have "ssl" error when activate counterfit, downgrade python to python 3.11
```bash
sudo apt update
sudo apt install -y software-properties-common
sudo apt-apt-repository ppa:deadsnakes/ppa
sudo apt update 
sudo apt install python3.11 python3.11-venv python3.11-dev
```
