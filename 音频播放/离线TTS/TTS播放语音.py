# -*- coding: UTF-8 -*-
import os
import pygame
import time
import pyttsx3
from time import strftime


curpath=os.path.dirname(__file__)
os.chdir(curpath)


engine = pyttsx3.init()
rate = engine.getProperty('rate')
engine.setProperty('rate', rate-70)#语速控制

#设置语音引擎
engine.setProperty('voice',r'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\VW Hui')
volume = engine.getProperty('volume')
engine.setProperty('volume', volume+0.5)#音量控制
engine.say("你好，李雅琪，好好学习啊！")
engine.runAndWait()

