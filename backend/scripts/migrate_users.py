import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models.models import User, Student, Teacher
from extensions import db

# 迁移用户数据到对应表
def migrate_users():
    with app.app_context():
        try:
            # 获取教师ID
            teacher_user = User.query.filter_by(role='teacher').first()
            if not teacher_user:
                print("错误: 没有找到教师用户!")
                return
            teacher_id = teacher_user.id
            print(f"使用教师ID: {teacher_id} ({teacher_user.nickname})")
            
            # 迁移学生数据
            print("\n开始迁移学生数据...")
            student_users = User.query.filter_by(role='student').all()
            for user in student_users:
                # 检查是否已存在对应的学生记录
                existing_student = Student.query.filter_by(phone=user.phone).first()
                if not existing_student:
                    # 创建学生记录
                    student = Student(
                        teacher_id=teacher_id,
                        name=user.nickname,
                        phone=user.phone,
                        age=18,  # 默认年龄，可根据实际情况调整
                        grade='初中',  # 默认年级，可根据实际情况调整
                        project='GESP C++',  # 默认项目，可根据实际情况调整
                        remaining_classes=0,
                        remaining_fee=0.0
                    )
                    db.session.add(student)
                    print(f"已创建学生记录: {user.nickname} ({user.phone})")
                else:
                    print(f"学生记录已存在: {user.nickname} ({user.phone})")
            
            # 迁移教师数据
            print("\n开始迁移教师数据...")
            teacher_users = User.query.filter_by(role='teacher').all()
            for user in teacher_users:
                # 检查是否已存在对应的教师记录
                existing_teacher = Teacher.query.filter_by(user_id=user.id).first()
                if not existing_teacher:
                    # 创建教师记录
                    teacher = Teacher(
                        user_id=user.id,
                        name=user.nickname,
                        phone=user.phone,
                        teaching_subject='GESP C++'
                    )
                    db.session.add(teacher)
                    print(f"已创建教师记录: {user.nickname} ({user.phone})")
                else:
                    print(f"教师记录已存在: {user.nickname} ({user.phone})")
            
            # 提交更改
            db.session.commit()
            print("\n数据迁移完成!")
            
        except Exception as e:
            print(f"迁移过程中出现错误: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()

if __name__ == '__main__':
    migrate_users()