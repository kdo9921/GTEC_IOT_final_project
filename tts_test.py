from gtts import gTTS
from playsound import playsound

s = gTTS(text = "TTS 테스트",lang='ko', slow=False)
s.save('sample.mp3')
playsound('sample.mp3')