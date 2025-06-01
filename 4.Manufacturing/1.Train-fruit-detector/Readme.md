This assignment receive data from counterfit or real sensor, processing by tflite, and then send result to adafruitIO feed
### How to run:
- Active virtual environemnt:
```bash
python -m venv .venv #create if not already available
```
```bash
source .venv/bin/activate
```
- install requirements: (can be skipped if done before)
```bash
pip install -r requirements.txt
```
- move to parent path of app.py
```bash
cd /workspaces/IoT-and-Smart-devices/4.Manufacturing/1.Train-fruit-detector
```
- run:
```bash
python app.py
```
# Notes:
- I used about 8k6 images to train this model, it may misrecognize for images containing fruit stems.
- Trained with only 11 types of fruit (apple, banana, dragon fruit, grapes, lemon, mango, orange, papaya, pineapple, pomegranate, strawberry).
