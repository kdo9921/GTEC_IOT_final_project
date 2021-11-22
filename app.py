import time
import aiy.device._led as LED
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

led = 'off'

@app.route('/',methods=('GET', 'POST'))
def index():
    global led
    return render_template('index.html', isLed=led)

@app.route('/api/led',methods=['POST'])
def ledToggle():
    global led
    print("LED 값 : " + led)
    if led == 'on':
        led = 'off'
        LED.controlLed(LED.LED_PIN1, LED.OFF)
        LED.controlLed(LED.LED_PIN2, LED.OFF)
        LED.controlLed(LED.LED_PIN3, LED.OFF)
        LED.controlLed(LED.LED_PIN4, LED.OFF)
    elif led == 'off':
        led = 'on'
        LED.controlLed(LED.LED_PIN1, LED.ON)
        LED.controlLed(LED.LED_PIN2, LED.ON)
        LED.controlLed(LED.LED_PIN3, LED.ON)
        LED.controlLed(LED.LED_PIN4, LED.ON)
    print("led 현재 상태 : " + led)
    return render_template('index.html', isLed=led)

if __name__=="__main__":
    GPIO.setmode(GPIO.BCM)
    LED.initLedModule()
    app.run(host="0.0.0.0", port="5000",debug=True)