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
    
    # 统计角色分布
    role_counts = {}
    for user in users:
        role = user.role
        if role not in role_counts:
            role_counts[role] = 0
        role_counts[role] += 1
    
    print('用户角色分布:')
    for role, count in role_counts.items():
        print(f'角色 "{role}": {count} 个用户')
    
    # 检查教师角色的用户
    print('\n教师角色用户:')
    teachers = User.query.filter_by(role='teacher').all()
    for teacher in teachers:
        print(f'ID: {teacher.id}, 用户名: {teacher.username}, 昵称: {teacher.nickname}, 角色: {teacher.role}')
    
    # 检查学生角色的用户
    print('\n学生角色用户:')
    students = User.query.filter_by(role='student').all()
    for student in students:
        print(f'ID: {student.id}, 用户名: {student.username}, 昵称: {student.nickname}, 角色: {student.role}')
    
    # 检查其他角色的用户
    print('\n其他角色用户:')
    other_users = User.query.filter(~User.role.in_(['teacher', 'student', 'admin'])).all()
    for user in other_users:
        print(f'ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}, 角色: {user.role}')
