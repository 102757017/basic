# -*- coding: UTF-8 -*-
import os
import sys
import subprocess




status = subprocess.run(["dir"],shell=True, capture_output=True,text=True )
print(status.stdout)
print(status.stderr)


