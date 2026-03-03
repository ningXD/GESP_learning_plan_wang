@echo off

rem 导航到项目目录
cd /d "%~dp0"

echo 正在激活虚拟环境...
call .venv\Scripts\Activate.bat

echo 正在安装依赖...
pip install -r backend\requirements.txt

echo 正在启动服务器...
python backend\start_server.py

pause