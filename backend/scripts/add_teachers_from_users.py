import sys
import os
import random
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from models.models import User, Teacher
from extensions import db

def add_teachers_from_users():
    """将users表中role为teacher的数据添加到teachers表中"""
    with app.app_context():
        try:
            # 获取所有role为teacher的用户
            teacher_users = User.query.filter_by(role='teacher').all()
            print(f"找到 {len(teacher_users)} 个教师用户")
            
            # 性别选项
            genders = ['男', '女']
            
            # 教学科目选项
            subjects = ['数学', '英语', '语文', '物理', '化学', '生物', '历史', '地理', '政治', '计算机', '美术', '音乐', '体育']
            
            added_count = 0
            skipped_count = 0
            
            for user in teacher_users:
                # 检查是否已存在对应的教师记录
                existing_teacher = Teacher.query.filter_by(user_id=user.id).first()
                if existing_teacher:
                    print(f"跳过已存在的教师: {user.nickname}")
                    skipped_count += 1
                    continue
                
                # 随机生成年龄（22-65岁）
                age = random.randint(22, 65)
                
                # 随机生成性别
                gender = random.choice(genders)
                
                # 随机生成教学科目
                teaching_subject = random.choice(subjects)
                
                # 创建教师记录
                new_teacher = Teacher(
                    user_id=user.id,
                    name=user.nickname,
                    gender=gender,
                    age=age,
                    phone=user.phone,
                    teaching_subject=teaching_subject
                )
                
                db.session.add(new_teacher)
                added_count += 1
                print(f"添加教师: {user.nickname}, 年龄: {age}, 科目: {teaching_subject}")
            
            # 提交事务
            db.session.commit()
            print(f"\n操作完成: 添加了 {added_count} 个教师，跳过了 {skipped_count} 个已存在的教师")
            
        except Exception as e:
            db.session.rollback()
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    add_teachers_from_users()