:echo off 是关闭下面所有命令的显示，bai但会显示自身
@echo off
echo 当前盘符：%~d0
echo 当前路径：%cd%
echo 当前执行命令行：%0
echo 当前bat文件路径：%~dp0
echo 当前bat文件短路径：%~sdp0
echo 当前bat文件路径下的子目录：%~sdp0子目录
echo 切换到当前脚步所在的目录
cd  %~dp0
pause