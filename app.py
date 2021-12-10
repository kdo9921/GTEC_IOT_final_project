import time
from threading import Thread
import aiy.device._led as LED
import aiy.device._fan as FAN
import RPi.GPIO as GPIO
import aiy.device._dht11 as DHT
import GPIO_EX
import pygame
import os
import telepot
import t_token
from gtts import gTTS

from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

PIR_PIN = 7
ON = 1
OFF = 0
ledArr = ['Off','Off','Off','Off']
ledPinArr = [LED.LED_PIN1,LED.LED_PIN2,LED.LED_PIN3,LED.LED_PIN4]
data = {'led':ledArr, 'temp':0, 'fan':'Off'}
pirState = 0
pir_value = "No"
isBC = False

def message(msg):
    bot = telepot.Bot(token=t_token.token)
    chat_id = t_token.id
    bot.sendMessage(chat_id=chat_id, text=msg)

def initGPIO():
    GPIO.setmode(GPIO.BCM)
    LED.initLedModule()
    FAN.initFan(FAN.FAN_PIN1,FAN.FAN_PIN2)
    GPIO_EX.setup(PIR_PIN, GPIO_EX.IN)
    offAll()
    getTemp()
    t = Thread(target=threadReadPir, args=())
    t.start()


def offAll():
    ledCtrl(0)
    FAN.controlFan(FAN.OFF)
    data['fan'] = 'Off'

def readPir(detect_state):
    global pirState, pir_value
    while detect_state:
        input_state = GPIO_EX.input(PIR_PIN)
        if input_state == True:
            if pirState == 0:
                pir_value = "Detected"
            pirState = 1
            return 1
        else:
            if pirState == 1:
                pir_value = "No"
            pirState = 0
            return 0

def threadReadPir():
    while True:
        readPir(ON)
        time.sleep(0.5)

def getTemp():
    global data
    temp = DHT.readTemp()
    data['temp'] = round(temp)

def voice():
    global data, isBC
    if isBC:
        return
    isBC = True
    str = "스마트 홈 제어를 시작합니다. 현재 온도는 {}도 입니다. ".format(data['temp'])
    if int(data['temp']) > 20:
        message("온도가 20도 이상입니다. 현재 온도 {}C".format(data['temp']))
    s = gTTS(text = str,lang='ko', slow=False)
    s.save('hello.mp3')
    os.system('mpg321 hello.mp3 &')
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
    voice()
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

@app.route('/api/temp',methods=['POST'])
def temp():
    global data
    getTemp()
    if int(data['temp']) > 20:
        message("온도가 20도 이상입니다. 현재 온도 {}C".format(data['temp']))
    return render_template('index.html', data=data)

currentMusic = {'isPlay': False, 'isPause' : False, 'index' : 0}
@app.route('/api/pir',methods=['POST'])
def pir():
    global pir_value
    return jsonify(result = pir_value)


currentMusic = {'isPlay': False, 'isPause' : False, 'index' : 0}
@app.route('/api/music',methods=['POST'])
def music():
    global currentMusic
    isPause = request.form.get('pause')
    isNext = request.form.get('next')
    music_list = os.listdir('music')
    music_list.sort()
    if isNext == "true":
        currentMusic['index'] += 1
        currentMusic['index'] = currentMusic['index'] % len(music_list)
        if currentMusic['isPause']:
            currentMusic['isPlay'] = False
        if currentMusic['isPlay']:
            pygame.mixer.music.stop()
            pygame.mixer.music.load("music/" + music_list[currentMusic['index']])
            pygame.mixer.music.play()
            message("노래 재생중 : " + music_list[currentMusic['index']])
    if isPause == "true":
        if currentMusic['isPlay']:
            if currentMusic['isPause']:
                currentMusic['isPause'] = False
                pygame.mixer.music.unpause()
            else:
                currentMusic['isPause'] = True
                pygame.mixer.music.pause()
        else:
            currentMusic['isPlay'] = True
            currentMusic['isPause'] = False
            pygame.mixer.music.load("music/" + music_list[currentMusic['index']])
            pygame.mixer.music.play()
            message("노래 재생중 : " + music_list[currentMusic['index']])
    return jsonify(result = currentMusic['isPause'])

if __name__=="__main__":
    initGPIO()
    pygame.mixer.init()
    app.run(host="0.0.0.0", port="8080",debug=True)