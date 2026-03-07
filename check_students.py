import sys
import os

# 添加backend目录到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from models.models import Student, User
from extensions import db
from app import app

with app.app_context():
    # 获取所有学生记录
    students = Student.query.all()
    print(f'Student表中有 {len(students)} 个学生记录')
    
    if students:
        print('\nStudent表中的学生记录:')
        for student in students:
            print(f'ID: {student.id}, 姓名: {student.name}, 电话: {student.phone}, 教师ID: {student.teacher_id}')
    else:
        print('\nStudent表中没有学生记录')
    
    # 获取所有用户表中的学生角色用户
    user_students = User.query.filter_by(role='student').all()
    print(f'\nUser表中有 {len(user_students)} 个学生角色用户')
    
    if user_students:
        print('\nUser表中的学生角色用户:')
        for user in user_students:
            print(f'ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}, 角色: {user.role}')
    
    # 检查是否有Student记录关联到教师
    teachers_with_students = set()
    for student in students:
        if student.teacher_id:
            teachers_with_students.add(student.teacher_id)
    
    print(f'\n有 {len(teachers_with_students)} 个教师有学生记录')
