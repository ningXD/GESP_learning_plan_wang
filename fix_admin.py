import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.models import User
from extensions import db
from app import app

with app.app_context():
    # 找到demo用户
    demo = User.query.filter_by(username='demo').first()
    if demo:
        print(f'修改前 - demo用户: 管理员={demo.admin}, 角色={demo.role}')
        # 更新admin字段为True
        demo.admin = True
        db.session.commit()
        print(f'修改后 - demo用户: 管理员={demo.admin}, 角色={demo.role}')
        print('demo用户已成功更新为管理员')
    else:
        print('demo用户不存在')
    
    # 也检查一下其他用户的admin字段
    print('\n检查其他用户的管理员状态:')
    users = User.query.filter_by(role='admin').all()
    for user in users:
        print(f'用户名: {user.username}, 管理员: {user.admin}')
