#!/usr/bin/python
# -*- coding: UTF-8 -*-
import pygame
import time


def play(mp3):
    try:
        pygame.mixer.init()
        track = pygame.mixer.music.load(mp3)
        pygame.mixer.music.play()
        time.sleep(1)
        #pygame.mixer.music.stop()   
    except pygame.error as e:
        print("该电脑没有声卡")

#mp3的采样率过高时，使用pygame播放会产生语速异常，需要用Adobe Audition修改mp3的采样率
play("a1.mp3")
