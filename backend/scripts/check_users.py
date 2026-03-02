import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.models import User

with app.app_context():
    users = User.query.all()
    print("当前用户列表:")
    print("-" * 60)
    for user in users:
        user_type = "管理员" if user.admin else ("教师" if user.role == "teacher" else "学生")
        print(f"ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}, 角色: {user.role}, 管理员: {user.admin}, 类型: {user_type}")
    print("-" * 60)
    print(f"总用户数: {len(users)}")
