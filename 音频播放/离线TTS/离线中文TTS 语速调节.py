#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pyttsx3
engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-50)#语速控制
engine.say('我的名字叫李雅琪')
engine.runAndWait()
    
