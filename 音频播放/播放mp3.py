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


play("a1.mp3")
