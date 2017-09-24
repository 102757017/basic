# -*- coding: UTF-8 -*-
import os
import sys

os.chdir(sys.path[0])
c1="sh & "

#查看当前 ls，相对于windows的dir命令
c2='ls'

#用默认浏览器打开百度
#c2=r"am start -a android.intent.action.VIEW -d http://www.baidu.com/"

#启动app,am start -n {packageName}/.{activityName}
#c2="am start -n org.openqa.selenium.android.app/org.openqa.selenium.android.app.MainActivity"

#杀死app
#c2="am kill org.openqa.selenium.android.app"

#读取或修改文件出现Permission denied解决方法，打开目标文件所在目录运行chmod 777 xxx.sh即可，对*.sh赋可执行的权限
#c2="chmod 777 test.txt"

#查看节点值，例如：
#c2='cat /sys/class/leds/lcd-backlight/brightness'

#修改节点值，此操作是覆盖模式，不是追加模式，例如：
#c2='echo 128 > test.txt'


#打印在ActivityManager标签里的日志 
#c2='logcat -s ActivityManager'

#测试端口通不通 telnet ip port,ping命令不能测试端口
#c2='telnet localhost 8080'

#看一下本机的44444端口状态:
#c2='netstat -anp | grep 444444'

c=c1+c2

os.system(c)

