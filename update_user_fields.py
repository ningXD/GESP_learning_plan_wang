import sys
import os
import random
import string

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.models import User
from extensions import db
from app import app

def generate_random_username(base_name, length=10):
    """生成随机用户名，基于基础名称加上随机字符"""
    # 移除基础名称中的特殊字符，只保留字母和数字
    base_name = ''.join(c for c in base_name if c.isalnum())
    # 生成随机字符
    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    # 组合基础名称和随机字符
    username = f"{base_name}_{random_chars}" if base_name else random_chars
    # 确保用户名长度不超过50字符
    return username[:50]

def generate_random_phone():
    """生成随机手机号"""
    # 生成以1开头的11位手机号
    return f"1{random.randint(3, 9)}{random.randint(1000000000, 9999999999)}"

def update_user_fields():
    """更新用户字段，确保username、phone、nickname字段不为空"""
    with app.app_context():
        # 获取所有用户
        users = User.query.all()
        print(f"找到 {len(users)} 个用户")
        
        updated_count = 0
        for user in users:
            updated = False
            
            # 检查并更新username
            if not user.username or user.username.strip() == '':
                # 基于nickname或role生成基础名称
                base_name = user.nickname or user.role or 'user'
                user.username = generate_random_username(base_name)
                updated = True
                print(f"更新用户ID {user.id} 的username为: {user.username}")
            
            # 检查并更新phone
            if not user.phone or user.phone.strip() == '':
                # 生成随机手机号
                user.phone = generate_random_phone()
                updated = True
                print(f"更新用户ID {user.id} 的phone为: {user.phone}")
            
            # 检查并更新nickname
            if not user.nickname or user.nickname.strip() == '':
                # 基于username或role生成nickname
                if user.username:
                    # 从username中提取基础名称作为nickname
                    nickname = user.username.split('_')[0] if '_' in user.username else user.username
                else:
                    nickname = user.role
                user.nickname = nickname
                updated = True
                print(f"更新用户ID {user.id} 的nickname为: {user.nickname}")
            
            # 检查并更新role
            if not user.role or user.role.strip() == '':
                user.role = 'student'  # 默认角色为学生
                updated = True
                print(f"更新用户ID {user.id} 的role为: {user.role}")
            
            if updated:
                updated_count += 1
        
        # 提交更改
        if updated_count > 0:
            db.session.commit()
            print(f"成功更新了 {updated_count} 个用户的字段")
        else:
            print("所有用户字段都已正确设置，无需更新")

if __name__ == '__main__':
    update_user_fields()
