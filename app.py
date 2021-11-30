import time
import aiy.device._led as LED
import aiy.device._fan as FAN
import RPi.GPIO as GPIO
import aiy.device._dht11 as DHT
from flask import Flask, render_template, request
app = Flask(__name__)

ledArr = ['Off','Off','Off','Off']
ledPinArr = [LED.LED_PIN1,LED.LED_PIN2,LED.LED_PIN3,LED.LED_PIN4]
data = {'led':ledArr, 'temp':0, 'fan':'Off'}

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    LED.initLedModule()
    FAN.initFan(FAN.FAN_PIN1,FAN.FAN_PIN2)
    offAll()
    getTemp()

def offAll():
    ledCtrl(0)
    FAN.controlFan(FAN.OFF)
    data['fan'] = 'Off'

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
        if ledArr[led] == 'Off':
            ledArr[led] = 'On'
            LED.controlLed(ledPinArr[led], LED.ON)
        else:
            ledArr[led] = 'Off'
            LED.controlLed(ledPinArr[led], LED.OFF)

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

if __name__=="__main__":
    initGPIO()
    app.run(host="0.0.0.0", port="5000",debug=True)