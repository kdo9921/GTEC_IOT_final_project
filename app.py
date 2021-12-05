import time
from threading import Thread
import aiy.device._led as LED
import aiy.device._fan as FAN
import RPi.GPIO as GPIO
import aiy.device._dht11 as DHT
import GPIO_EX

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

PIR_PIN = 7
ON = 1
OFF = 0
ledArr = ['Off','Off','Off','Off']
ledPinArr = [LED.LED_PIN1,LED.LED_PIN2,LED.LED_PIN3,LED.LED_PIN4]
data = {'led':ledArr, 'temp':0, 'fan':'Off'}
pirState = 0

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    LED.initLedModule()
    FAN.initFan(FAN.FAN_PIN1,FAN.FAN_PIN2)
    GPIO_EX.setup(PIR_PIN, GPIO_EX.IN)
    offAll()
    getTemp()

def offAll():
    ledCtrl(0)
    FAN.controlFan(FAN.OFF)
    data['fan'] = 'Off'

def readPir(detect_state):
    global pirState
    while detect_state:
        input_state = GPIO_EX.input(PIR_PIN)
        if input_state == True:
            if pirState == 0:
                print("Motion Detected.")
            pirState = 1
            return 1
        else:
            if pirState == 1:
                print("Motion Ended.")
            pirState = 0
            return 0

def threadReadPir():
    while True:
        readPir(ON)
        time.sleep(0.5)

def getTemp():
    global data
    data['temp'] = DHT.readTemp()

def ledCtrl(led):
    global ledArr
    if led == 0:
        for i in range(len(ledArr)):
            ledArr[i] = 'Off'
            LED.controlLed(ledPinArr[i], LED.OFF)
    elif led == 5:
        for i in range(len(ledArr)):
            ledArr[i] = 'On'
            LED.controlLed(ledPinArr[i], LED.ON)
    else:
        if ledArr[led-1] == 'Off':
            ledArr[led-1] = 'On'
            LED.controlLed(ledPinArr[led-1], LED.ON)
        else:
            ledArr[led-1] = 'Off'
            LED.controlLed(ledPinArr[led-1], LED.OFF)

@app.route('/',methods=('GET', 'POST'))
def index():
    global data
    return render_template('index.html', data=data)

@app.route('/api/led',methods=['POST'])
def ledToggle():
    global data
    led = int(request.form.get('led'))
    ledCtrl(led)
    return render_template('index.html', data=data)

@app.route('/api/fan',methods=['POST'])
def fanToggle():
    global data
    if data['fan'] == 'On':
        data['fan'] = 'Off'
        FAN.controlFan(FAN.OFF)
    elif data['fan'] == 'Off':
        data['fan'] = 'On'
        FAN.controlFan(FAN.ON)
    return render_template('index.html', data=data)

@app.route('/api/outing',methods=['POST'])
def outing():
    global data
    offAll()
    return render_template('index.html', data=data)

@app.route('/api/fan',methods=['POST'])
def temp():
    global data
    getTemp()
    return render_template('index.html', data=data)

@app.route('/api/pir',methods=['POST'])
def pir():
    global pirState
    pir_value = "No"
    if pirState == 0:
        pir_value = "Detected"
    return jsonify(result = pir_value)


if __name__=="__main__":
    initGPIO()
    t = Thread(target=threadReadPir, args=())
    t.start()
    app.run(host="0.0.0.0", port="5000",debug=True)