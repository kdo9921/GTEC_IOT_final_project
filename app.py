import time
import aiy.device._led as LED
import aiy.device._fan as FAN
import RPi.GPIO as GPIO
import aiy.device._dht11 as DHT
from flask import Flask, render_template, request
app = Flask(__name__)

ledArr = [False,False,False,False]
ledPinArr = [LED.LED_PIN1,LED.LED_PIN2,LED.LED_PIN3,LED.LED_PIN4]
data = {'led':ledArr, 'temp':0, 'fan':'off'}

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    LED.initLedModule()
    FAN.initFan(FAN.FAN_PIN1,FAN.FAN_PIN2)

def getTemp():
    global data
    data['temp'] = DHT.readTemp()

def ledCtrl(led):
    global ledArr
    if led == 0:
        for i in range(len(ledArr)):
            ledArr[i] = False
            LED.controlLed(ledPinArr[i], LED.OFF)
    elif led == 5:
        for i in range(len(ledArr)):
            ledArr[i] = True
            LED.controlLed(ledPinArr[i], LED.ON)
    else:
        if ledArr[led] == False:
            ledArr[led] = True
            LED.controlLed(ledPinArr[led], LED.ON)
        else:
            ledArr[led] = False
            LED.controlLed(ledPinArr[led], LED.OFF)


    return

@app.route('/',methods=('GET', 'POST'))
def index():
    global data
    return render_template('index.html', data=data)

@app.route('/api/led',methods=['POST'])
def ledToggle():
    global data
    led = request.form.get('led')
    #ledCtrl(led)
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