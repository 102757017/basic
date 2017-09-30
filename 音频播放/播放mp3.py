# -*- coding: UTF-8 -*-
import os
import pygame
import time


curpath=os.path.dirname(__file__)
os.chdir(curpath)


#播放mp3
def play_c(a):
    pygame.mixer.init()
    track = pygame.mixer.music.load(a)
    pygame.mixer.music.play()
    time.sleep(0.8)
    pygame.mixer.music.stop()

play_c('a1.mp3')
