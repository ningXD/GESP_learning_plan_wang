import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.models import User
from extensions import db
from app import app

with app.app_context():
    # 获取所有用户
    users = User.query.all()
    print('用户列表:')
    for user in users:
        print(f'ID: {user.id}, 用户名: {user.username}, 角色: {user.role}, 管理员: {user.admin}')
    
    # 检查demo用户
    print('\n检查demo用户:')
    demo = User.query.filter_by(username='demo').first()
    if demo:
        print(f'demo用户 - 管理员: {demo.admin}')
        print(f'demo用户 - 角色: {demo.role}')
    else:
        print('demo用户不存在')
