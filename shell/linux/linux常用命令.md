#### 快捷键

tab 补全命令，补全路径

Ctrl+c  在命令行下起着终止当前执行程序的作用,

Ctrl+d 相当于exit命令

ctrl+z ：挂起，把服务切换到后台并且暂停

jobs ：查看被挂起的程序工作号

bg  工作号 ： 将挂起的作业放到后台执行

fg  工作号 ：将挂起的作业放回到前台执行



#### --help命令

查询命令的基本用法

```
ps --help
```



#### man命令

查看命令的详细用法

```
man ls
```



#### echo命令

定向输出到文件，如果文件不存在，就创建文件；

**">":**此操作是覆盖模式，如果文件存在，就将其清空重新写入

**">>":**此操作是追加模式，如果文件存在，则将新的内容追加到那个文件的末尾，该文件中的原有内容不受影响。

```
echo 128
echo 128 > test.txt
echo 128 >> test.txt
```



### 文件相关命令

#### ls命令

查看当前路径下的文件，相对于windows的dir命令

-a：显示隐藏文件

-lh：查看当前目录下文件属性

```
ls -a
ls -l ./sample_data
ls -lh
```



#### tree命令

查看树形目录结构，需要先安装模块tree

```
apt-get install tree -y
tree
```



#### mkdir命令

创建文件夹

文件夹前面加个“.”,表示隐藏文件夹

```
mkdir .hide
```





#### ldd命令

列出一个程序所需要得动态链接库

```
ldd /bin/ls 
```



#### which命令

查询运行文件所在路径：

```
which python3
```





#### rm命令

删除非空文件夹

```
rm -rf /tmp/aaa
```



#### cp命令

复制文件

```
cp /etc/apt/sources.list /etc/apt/sources.list.back
```



#### cat命令

查看文件内容

```
cat /sys/class/leds/lcd-backlight/brightness
```



#### sed命令

替换文件内的文本

紧跟着s命令字符被认为是分隔符

末尾加g替换每一个匹配的关键字,否则只替换每行的第一个

```
sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
sed -i s:raspbian.raspberrypi.org:mirrors.tuna.tsinghua.edu.cn/raspbian:g /etc/apt/sources.list
```



#### ln命令

-s:创建软链接：在target文件夹下创建快捷方式aa，指向/source

无参数:创建硬链接

```
ln -s /source /target/aa
ln /source /target/bb
```



#### wget命令

下载文件,用-P指定保存目录名

```
wget -P /home/user/test http://cn.wordpress.org/wordpress-3.1-zh_CN.zip
```





### 权限命令

#### chmod命令

修改文件权限。读取或修改文件出现Permission denied解决方法

-R：修改文件夹包括子目录的权限

```
chmod 777 test.txt
chmod -R 777 path
```



#### chown命令

修改文件权属

```
chown root test.txt
```



#### chgrp命令

修改文件群组

```
chgrp root test.txt
```



```
#创建群组
groupadd group1
#创建用户
useradd user1 -m -s /bin/bash -d /home/username -g group1
#创建用户密码
sudo passwd user1
#切换用户
su - user1

```



### 网络命令

#### ifconfig命令

显示ip地址

```
ifconfig
```



#### telnet命令

测试端口通不通 ,telnet本机端口是不通的

telnet协议是基于TCP端口,所以UDP的端口即使是开放的也无回应

```
telnet localhost 8080
```



#### netstat命令

看一下本机的44444端口状态

```
netstat -anp | grep 444444
```



#### nslookup命令

测试dns解析

```
nslookup www.baidu.com 114.114.114.114
nslookup www.baidu.com 114.114.114.114#53
```



#### dig命令

测试dns解析

测试域名是否被dns污染，可以指定一个不存在的dns服务器，理应没有任何返回。但我们却得到了一个返回ip。可见这个域名已经被DNS污染了。

测试dns服务器是否存在：telnet 144.223.234.234 53

```
dig @114.114.114.114 www.baidu.com
dig @144.223.234.234 www.google.com
```



#### iptables命令：

| 选项                     | 描述                                             |
| ------------------------ | ------------------------------------------------ |
| -A  --append             | 将一个或多个规则添加到所选链的末尾。             |
| -C --check               | 检查与所选链中的规范匹配的规则。                 |
| -D --delete              | 从所选链中删除一个或多个规则。                   |
| -F --flush               | 清空，逐个删除所有规则。                         |
| -I --insert              | 将一个或多个规则作为给定的规则编号插入所选链中。 |
| -L --list                | 查看，显示所选链中的规则。                       |
| -n --numeric             | 以数字格式显示IP地址或主机名和邮政编号。         |
| -N --new-chain <name>    | 创建一个新的用户定义链。                         |
| -v --verbose             | 与list选项一起使用时提供更多信息。               |
| -X --delete-chain <name> | 删除用户定义的链。                               |
| -R                       | 修改                                             |

| 参数                | 描述                                             |
| ------------------- | ------------------------------------------------ |
| -p, --protocol      | 协议，如TCP，UDP等。                             |
| -s, --source        | 来源地址，可以是地址，网络名称，主机名等。       |
| -d, --destination   | 目的地址，可以是地址，网络名称，主机名等。       |
| -j, --jump          | 指定规则的目标; 即如果数据包匹配该怎么办。       |
| -g, --goto chain    | 指定过程将在用户指定的链中继续处理。             |
| -i, --in-interface  | 命名接收数据包的接口。Ifconfig可以查看接口       |
| -o, --out-interface | 发送数据包的接口名称。                           |
| -f, --fragment      | 该规则仅适用于分段数据包的第二个和后续片段。     |
| -c, --set-counters  | 使管理员能够以一条规则初始化数据包和字节计数器。 |
| -n                  | 不做解析                                         |
| -t                  | 表名                                             |
| -v                  | verbose mode                                     |
| --line              | 显示规则编号                                     |

input–用于处理“进入”路由器的数据包，即数据包目标IP地址是到达路由器一个接口的IP地址，“经过”路由器的数据包不会在input-chains处理（这里要注意理解的是“进入”和“经过”的不同意味）
forward– 用于处理“通过”路由器的数据包，只对不是访问本机，但是要通过这台机器转发的包有效
output– 用于处理源于路由器并从其中一个接口出去的数据包。

![](https://gitee.com/sunny_ho/image_bed/raw/master/img/20200613225128.png)

openwrt监控某个ip
添加一个新的iptables chain

```
iptables -N P45
```

往刚才建的P45和delegate_forward添加rules，ip换成你想监控的

-I 代表chain
-s source
-d destination
-j 如果符合就

```
iptables -I P45 -s 192.168.111.115 -j ACCEPT
iptables -I P45 -d 192.168.111.115 -j ACCEPT
iptables -I forwarding_rule -s 192.168.111.115 -j P45
iptables -I forwarding_rule -d 192.168.111.115 -j P45
```

在iptable中允许22号端口

```
iptables -I INPUT -p tcp --dport 22 -j ACCEPT
```



### Android专用adb命令

#### start命令

启动app

语法：am start -n {packageName}/.{activityName}

```
am start -n org.openqa.selenium.android.app/org.openqa.selenium.android.app.MainActivity
```

用默认浏览器打开百度

```
am start -a android.intent.action.VIEW -d http://www.baidu.com/
```

#### force-stop命令

杀死app

```
am force-stop org.openqa.selenium.android.app
```



#### logcat命令

打印在ActivityManager标签里的日志 

```
logcat -s ActivityManager
```

