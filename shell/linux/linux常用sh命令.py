# -*- coding: UTF-8 -*-
import os
import sys

os.chdir(sys.path[0])
c1="sh & "

#查看当前 ls，相对于windows的dir命令
c2='ls'

#查看当前绝对路径
#c2='pwd'

#查看隐藏文件
#c2='ls -a'

#查看sample_data文件夹的内容
#c2="ls -l ./sample_data"

#查看树形目录结构，需要先安装模块，apt-get install tree -y
#c2="tree"

#生成隐藏文件夹,文件夹前面加个“.”,表示隐藏文件
#c2='mkdir .hide'

#下载文件,用-P指定保存目录名
#c2="wget -P /home/user/test http://cn.wordpress.org/wordpress-3.1-zh_CN.zip"

#显示ip地址
#c2=r"ifconfig"

#用默认浏览器打开百度
#c2=r"am start -a android.intent.action.VIEW -d http://www.baidu.com/"

#启动app,am start -n {packageName}/.{activityName}
#c2="am start -n org.openqa.selenium.android.app/org.openqa.selenium.android.app.MainActivity"

#杀死app
#c2="am force-stop org.openqa.selenium.android.app"

#读取或修改文件出现Permission denied解决方法，打开目标文件所在目录运行chmod 777 xxx.sh即可，对*.sh赋可执行的权限
#c2="chmod 777 test.txt"

#查看节点值，例如：
#c2='cat /sys/class/leds/lcd-backlight/brightness'

#定向输出到文件，如果文件不存在，就创建文件；如果文件存在，就将其清空,">"此操作是覆盖模式，不是追加模式，
#c2='echo 128 > test.txt'

#将输出内容追加到目标文件中。如果文件不存在，就创建文件；如果文件存在，则将新的内容追加到那个文件的末尾，该文件中的原有内容不受影响。
#c2='echo 128 >> test.txt'


#打印在ActivityManager标签里的日志 
#c2='logcat -s ActivityManager'

#测试端口通不通 telnet ip port,ping命令不能测试端口
#c2='telnet localhost 8080'

#看一下本机的44444端口状态:
#c2='netstat -anp | grep 444444'

#在iptable中允许22号端口:
#c2='iptables -I INPUT -p tcp --dport 22 -j ACCEPT'

#创建软链接：在target文件夹下创建快捷方式aa，指向/source
#c2='ln -s /source /target/aa'

#创建硬链接
#c2='ln /source /target/bb'

#查看当前目录下文件属性
#c2='ls -lh'

#修改文件权限
#c2='chmod 777 test.txt'

#修改文件夹包括子目录的权限
#c2='chmod -R 777 path'

#修改文件权属，
#c2='chown root test.txt'

#修改文件群组，
#c2='chgrp root test.txt'


c=c1+c2

os.system(c)
