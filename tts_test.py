from gtts import gTTS
import os
import pygame

s = gTTS(text = "TTS 테스트 123",lang='ko', slow=False)
s.save('sample.mp3')

pygame.mixer.init() #mixer 모듈 초기화
p = pygame.mixer.Sound('relations.wav') 
p.play(-1)
#os.system('mpg321 relations.wav &')
while True:
    a = 1