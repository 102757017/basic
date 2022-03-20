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



### shell编程

#### 一般变量赋值

变量名必须以字母或者下划线开头，不能使用 Shell 里的关键字，（通过 help 命令可以查看保留关键字）

注意，赋值号`=`的周围不能有空格

```
a="我是一个变量"
echo $a
#加花括号是可以帮助解释器识别变量的边界
echo ${a}b
```

以单引号`' '`包围变量的值时，单引号里面是什么就输出什么，即使内容中有变量和命令（命令需要反引起来）也会把它们原样输出。这种方式比较适合定义显示纯字符串的情况，即不希望解析变量、命令等的场景。

以双引号`" "`包围变量的值时，输出时会先解析里面的变量和命令。

```
#!/bin/bash
url="http://c.biancheng.net"
website1='C语言中文网：${url}'
website2="C语言中文网：${url}"
echo $website1
echo $website2
```

#### 特殊变量

$?上个命令的退出状态，或函数的返回值。大部分命令执行成功会返回 0，失败返回 1。

```
ping -c 2 192.168.1.1
echo $?
```



将命令的执行结果赋值给变量，把命令用`$()`包围起来

```
variable=$(ls)
```

#### 逻辑运算

使用方法：test EXPRESSION

**注意：所有字符 与逻辑运算符直接用“空格”分开，不能连到一起。**

```
test 1 = 1 && echo 'ok'
```

精简表达式 [] 

在[] 表达式中，[]与变量也需要用空格分开，不能连到一起，常见的>,<需要加转义字符，或者使用[[]]

```
[ 1 = 1 ] && echo 'ok'
[ 2 \> 1 ] && echo 'ok'
[[ 2 > 1 ]] && echo 'ok'
```



#### if 语句

$[]和$(())是一样的，都是进行数学运算的。支持+ - * / %（“加、减、乘、除、取模”）。但是注意，bash只能作整数运算，对于浮点数是当作字符串处理的。

```
a=2
b=1
if  [[ $a == $b ]]
then
    echo 'a=b'
else
    echo 'a!=b'
fi
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



#### >命令

将命令的执行结果输出到指定位置，覆盖模式

创建一个空文件

```
echo ""> new.txt
```



#### >>命令

将命令的执行结果输出到指定位置，追加模式

创建一个空文件

```
echo "">> new.txt
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

通过 cat>>文件<<EOF EOF 来实现文件追加多行内容

```
cat>>filename.txt<<EOF
hello world
代码改变世界 Coding Changes the World
她买了张彩票，中了3,300多万美元。
EOF
```



#### sed命令

替换文件内的文本

紧跟着s命令字符被认为是分隔符

末尾加g替换每一个匹配的关键字,否则只替换每行的第一个

```
sed -i s/archive.ubuntu.com/mirrors.aliyun.com/g /etc/apt/sources.list
sed -i s:raspbian.raspberrypi.org:mirrors.tuna.tsinghua.edu.cn/raspbian:g /etc/apt/sources.list
```

直接匹配Defaults  env_reset匹配不到，需要使用\s\+匹配连续的空格

```
sudo sed -i 's/Defaults\s\+env_reset/Defaults !env_reset/g' /etc/sudoers
```



在每行的行尾添加字符，"$"代表行尾，比如“TAIL”，命令如下：

$a表示尾行后新增

$i表示尾行前新增

追加多行时在行与行之间才需要添加换行符

```
echo ""> high.txt
sed -i '$a 追加1行' high.txt
sed -i '$a 追加2行，此为第1行\n此为第二行' high.txt
cat high.txt
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



#### 创建群组、用户

```
#创建群组
groupadd group1
#创建用户
useradd user1 -m -s /bin/bash -d /home/username -g group1
#创建用户密码
sudo passwd user1

#切换用户
su - user1
#删除用户
userdel pi
```



### 系统设置

#### export命令

#加入环境变量

```
export PATH="${PATH}:/opt/crosstool/bin"
```



#### sudo命令

#以user1的权限运行命令

```
sudo -u user1 env
```

#以root的权限运行命令

```
sudo env
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



#### git命令

克隆代码库

```
git clone https://hub.fastgit.org/jcmvbkbc/crosstool-NG.git
```

克隆指定分支

```
git clone -b v2.8.1 https://git.oschina.net/oschina/android-app.git
```

使用镜像站加速

```
git config --global url."https://github.com.cnpmjs.org/".insteadOf https://github.com/
git config --global --unset url.https://github.com/.insteadof
```

使用 `clone` 指令的时候这些子模块 `submodule` 并不会自动下载，因为他们在另外的地址中存放。你需要 `clone` 完目标项目后，执行

要加速submodule的下载速度，需要将原项目.git/config中使用的 `submodule` 模块的链接地址修改为子模块迁移到gitee中后的地址

```
git submodule update --init --recursive
```



#### sshpass命令

首先安装工具

```
sudo apt-get install sshpass
```

本地执行远程机器的命令

```
sshpass -p 密码 ssh root@192.168.1.1 ifconfig
```

从远程主机上拉取文件到本地

```
sshpass -p 密码 scp root@192.168.1.1:/etc/config/shadowsocksr_back /home/pi/pythonapp/ss_nude/shadowsocksr
```

上传文件到远程主机

```
sshpass -p 密码 scp /home/pi/pythonapp/ss_nude/shadowsocksr root@192.168.1.1:/etc/config/shadowsocksr
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

