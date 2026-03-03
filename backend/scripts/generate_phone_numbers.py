#!/usr/bin/env python3
"""
为数据库中现有的用户生成手机号
"""
import sys
import os
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.models import User
from extensions import db

def generate_phone_number():
    """生成随机手机号"""
    # 中国手机号前缀
    prefixes = ['130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
                '150', '151', '152', '153', '155', '156', '157', '158', '159',
                '170', '171', '173', '175', '176', '177', '178',
                '180', '181', '182', '183', '184', '185', '186', '187', '188', '189']
    
    prefix = random.choice(prefixes)
    suffix = ''.join(random.choices('0123456789', k=8))
    return f"{prefix}{suffix}"

def main():
    """为没有手机号的用户生成手机号"""
    with app.app_context():
        # 查询所有没有手机号的用户
        users = User.query.filter(User.phone.is_(None) | (User.phone == '')).all()
        
        print(f"找到 {len(users)} 个没有手机号的用户")
        
        for user in users:
            # 生成随机手机号
            phone = generate_phone_number()
            user.phone = phone
            print(f"为用户 {user.username} 生成手机号: {phone}")
        
        # 提交更改
        if users:
            db.session.commit()
            print(f"成功为 {len(users)} 个用户生成手机号")
        else:
            print("所有用户都已有手机号，无需生成")

if __name__ == '__main__':
    main()
