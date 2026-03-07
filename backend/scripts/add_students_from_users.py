import sys
import os
import random
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from models.models import User, Student
from extensions import db

def add_students_from_users():
    """将users表中role为student的数据添加到students表中"""
    with app.app_context():
        try:
            # 获取所有role为student的用户
            student_users = User.query.filter_by(role='student').all()
            print(f"找到 {len(student_users)} 个学生用户")
            
            # 获取一个默认教师ID（如果存在）
            default_teacher_id = None
            teacher_user = User.query.filter_by(role='teacher').first()
            if teacher_user:
                default_teacher_id = teacher_user.id
                print(f"使用默认教师ID: {default_teacher_id}")
            else:
                # 如果没有教师，使用admin用户作为默认
                admin_user = User.query.filter_by(role='admin').first()
                if admin_user:
                    default_teacher_id = admin_user.id
                    print(f"使用默认管理员ID: {default_teacher_id}")
                else:
                    print("警告: 没有找到教师或管理员用户，将使用ID 1作为默认值")
                    default_teacher_id = 1
            
            # 年级选项
            grades = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '初一', '初二', '初三', '高一', '高二', '高三']
            
            # 性别选项
            genders = ['男', '女']
            
            added_count = 0
            skipped_count = 0
            
            for user in student_users:
                # 检查是否已存在相同name的学生
                existing_student = Student.query.filter_by(name=user.nickname).first()
                if existing_student:
                    print(f"跳过已存在的学生: {user.nickname}")
                    skipped_count += 1
                    continue
                
                # 随机生成年龄（6-18岁）
                age = random.randint(6, 18)
                
                # 随机生成年级
                grade = random.choice(grades)
                
                # 随机生成性别
                gender = random.choice(genders)
                
                # 创建学生记录
                new_student = Student(
                    teacher_id=default_teacher_id,
                    name=user.nickname,
                    gender=gender,
                    age=age,
                    grade=grade,
                    phone=user.phone,
                    created_at=user.created_at  # 保持创建时间一致
                )
                
                db.session.add(new_student)
                added_count += 1
                print(f"添加学生: {user.nickname}, 年龄: {age}, 年级: {grade}")
            
            # 提交事务
            db.session.commit()
            print(f"\n操作完成: 添加了 {added_count} 个学生，跳过了 {skipped_count} 个已存在的学生")
            
        except Exception as e:
            db.session.rollback()
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_students_from_users()