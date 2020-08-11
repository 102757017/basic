# -*- coding: UTF-8 -*-
import sys,os
print('hello')
print(__file__)



if getattr( sys, 'frozen', False ) :
        bundle_dir=sys._MEIPASS
else :
        bundle_dir=os.path.dirname(os.path.abspath(__file__))
print(bundle_dir)
