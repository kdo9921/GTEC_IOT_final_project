import time
import aiy.device._led as LED
import aiy.device._fan as FAN
import RPi.GPIO as GPIO
import aiy.device._dht11 as DHT
from flask import Flask, render_template, request
app = Flask(__name__)

data = {'led':'off', 'temp':0, 'fan':'off'}

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    LED.initLedModule()
    FAN.initFan(FAN.FAN_PIN1,FAN.FAN_PIN2)

def getTemp():
    global data
    data['temp'] = DHT.readTemp()

@app.route('/',methods=('GET', 'POST'))
def index():
    global data
    return render_template('index.html', data=data)

@app.route('/api/led',methods=['POST'])
def ledToggle():
    global data
    if data['led'] == 'on':
        data['led'] = 'off'
        LED.controlLed(LED.LED_PIN1, LED.OFF)
        LED.controlLed(LED.LED_PIN2, LED.OFF)
        LED.controlLed(LED.LED_PIN3, LED.OFF)
        LED.controlLed(LED.LED_PIN4, LED.OFF)
    elif data['led'] == 'off':
        data['led'] = 'on'
        LED.controlLed(LED.LED_PIN1, LED.ON)
        LED.controlLed(LED.LED_PIN2, LED.ON)
        LED.controlLed(LED.LED_PIN3, LED.ON)
        LED.controlLed(LED.LED_PIN4, LED.ON)
    return render_template('index.html', data=data)

@app.route('/api/fan',methods=['POST'])
def fanToggle():
    global data
    if data['fan'] == 'on':
        data['fan'] = 'off'
        FAN.controlFan(FAN.OFF)
    elif data['fan'] == 'off':
        data['fan'] = 'on'
        FAN.controlFan(FAN.ON)
    return render_template('index.html', data=data)

if __name__=="__main__":
    initGPIO()
    getTemp()
    app.run(host="0.0.0.0", port="5000",debug=True)