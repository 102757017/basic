# -*- coding: UTF-8 -*-
from baiToVoice import BaiVoice
import os
import sys

os.chdir(sys.path[0])
# 这里使用的是作者自己的appId,appKey及secretKey，建议正式开发不要使用默认的，请调用
# BaiVoice(appId, appKey,secretKey)
bai_voice = BaiVoice()
bai_voice.change_voice_style(per=3)
'''
bai_voice.change_voice_style(可选参数):
spd:设置语速，取值范围是0-9。
pit: 设置语调，取值范围是0-9。
vol:设置音量，取值范围是0-15。
per:发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫。
'''

# 保存MP3文件
bai_voice.translate_output_mp3_file("条码打印机选定的程序与作动治具不一致，请核对程序号",'语音.mp3')
#os.system('fengyu.mp3')
