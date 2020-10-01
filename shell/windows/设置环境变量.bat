echo 1. 设置临时环境变量(覆盖模式)
set BAT_HOME=c:\bat

echo 2. 设置临时环境变量(追加模式)
set BAT_HOME=c:\bat
set BAT_HOME=%BAT_HOME%;c:\bat

echo 3. 设置永久环境变量(覆盖模式)
setx /M "BAT_HOME" "c:\bat"

echo 4. 设置永久环境变量(追加模式)，将在新打开的终端中生效,当前终端不会立即生效
echo 在 win10 下请右键选择管理员身份运行。
echo /M 是选择系统的意思，在 win10 下面是会严格区分系统环境变量和用户环境变量的，默认的是用户环境变量，所以，如果要修改系统环境变量，那么就需要加上这个指令.
echo PATH 是路径的意思，意思是我要设置的参数是PATH.
setx /M Path "%Path%;D:\ProgramData\Anaconda3;D:\ProgramData\Anaconda3\Scripts;D:\ProgramData\Anaconda3\Library\bin"

cmd /k echo.