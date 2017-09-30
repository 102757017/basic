#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')
for voice in voices:
   engine.setProperty('voice', voice.id)
   print(voice.id)
   print(type(voice.id))
   engine.say('我的名字叫李雅琪')
engine.runAndWait()
