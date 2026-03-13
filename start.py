import os
import sys

# 切换到backend目录
os.chdir('backend')

# 运行app.py
sys.executable = sys.executable
os.system(f"{sys.executable} app.py")