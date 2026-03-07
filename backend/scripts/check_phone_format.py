import sys
import os
import re

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from models.models import User, Student, Teacher
from extensions import db

def is_valid_phone(phone):
    """检查手机号格式是否正确"""
    # 中国大陆手机号格式：1开头的11位数字
    pattern = r'^1[3-9]\d{9}$'
    return bool(re.match(pattern, phone))

def check_phone_formats():
    """检查所有表中的手机号格式"""
    with app.app_context():
        try:
            print("=== 检查手机号格式 ===")
            
            # 检查users表
            print("\n1. Users表:")
            users = User.query.all()
            user_invalid = 0
            for user in users:
                if not is_valid_phone(user.phone):
                    print(f"  无效手机号: ID={user.id}, Phone={user.phone}, Role={user.role}")
                    user_invalid += 1
            print(f"  总计: {len(users)} 条记录, 无效: {user_invalid} 条")
            
            # 检查students表
            print("\n2. Students表:")
            students = Student.query.all()
            student_invalid = 0
            for student in students:
                if not is_valid_phone(student.phone):
                    print(f"  无效手机号: ID={student.id}, Phone={student.phone}, Name={student.name}")
                    student_invalid += 1
            print(f"  总计: {len(students)} 条记录, 无效: {student_invalid} 条")
            
            # 检查teachers表
            print("\n3. Teachers表:")
            teachers = Teacher.query.all()
            teacher_invalid = 0
            for teacher in teachers:
                if not is_valid_phone(teacher.phone):
                    print(f"  无效手机号: ID={teacher.id}, Phone={teacher.phone}, Name={teacher.name}")
                    teacher_invalid += 1
            print(f"  总计: {len(teachers)} 条记录, 无效: {teacher_invalid} 条")
            
            total_invalid = user_invalid + student_invalid + teacher_invalid
            total_records = len(users) + len(students) + len(teachers)
            print(f"\n=== 总览 ===")
            print(f"总记录数: {total_records}")
            print(f"无效手机号数: {total_invalid}")
            print(f"有效手机号数: {total_records - total_invalid}")
            
        except Exception as e:
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_phone_formats()