echo 设置临时环境变量
set Path=%Path%;D:\hewei\Python36-32
set Path=%Path%;D:\hewei\Python36-32\Scripts

echo 使用清华源
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
python -m pip install --upgrade pip

cmd /k echo.