import sys
import os
from datetime import datetime
import bcrypt

# 添加backend目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入所需模块
from extensions import db
from models.models import User, Student, Teacher

# 初始化数据库
def init_db():
    from app import app
    with app.app_context():
        return app

# 同步用户表数据
def sync_user_tables():
    app = init_db()
    
    with app.app_context():
        print("开始同步用户表数据...")
        
        # 创建教师表（如果不存在）
        try:
            db.create_all()
            print("教师表创建成功")
        except Exception as e:
            print(f"创建教师表时出错: {e}")
        
        # 同步学生数据：确保所有users表中role为student的用户都在students表中有记录
        print("\n同步学生数据...")
        student_users = User.query.filter_by(role='student').all()
        print(f"users表中共有 {len(student_users)} 个学生用户")
        
        student_count = 0
        for user in student_users:
            # 检查是否已存在
            existing_student = Student.query.filter_by(phone=user.phone).first()
            if not existing_student:
                # 创建学生记录
                student = Student(
                    teacher_id=1,  # 默认教师ID
                    name=user.nickname or user.username,
                    gender=user.gender,
                    age=user.age,
                    grade=user.grade,
                    project=user.subject,
                    phone=user.phone
                )
                db.session.add(student)
                student_count += 1
                
                if student_count % 10 == 0:
                    db.session.commit()
                    print(f"已同步 {student_count} 个学生")
        
        db.session.commit()
        print(f"学生数据同步完成，新增 {student_count} 个学生记录")
        
        # 同步教师数据：确保所有users表中role为teacher的用户都在teachers表中有记录
        print("\n同步教师数据...")
        teacher_users = User.query.filter_by(role='teacher').all()
        print(f"users表中共有 {len(teacher_users)} 个教师用户")
        
        teacher_count = 0
        for user in teacher_users:
            # 检查是否已存在
            existing_teacher = db.session.query(Teacher).filter_by(user_id=user.id).first()
            if not existing_teacher:
                # 创建教师记录
                teacher = Teacher(
                    user_id=user.id,
                    gender=user.gender,
                    age=user.age,
                    phone=user.phone,
                    teaching_subject=user.subject
                )
                db.session.add(teacher)
                teacher_count += 1
                
                if teacher_count % 10 == 0:
                    db.session.commit()
                    print(f"已同步 {teacher_count} 个教师")
        
        db.session.commit()
        print(f"教师数据同步完成，新增 {teacher_count} 个教师记录")
        
        # 检查最终数据
        total_students = Student.query.count()
        total_teachers = db.session.query(Teacher).count()
        total_student_users = User.query.filter_by(role='student').count()
        total_teacher_users = User.query.filter_by(role='teacher').count()
        
        print(f"\n同步完成！")
        print(f"users表中学生用户: {total_student_users}")
        print(f"students表中记录: {total_students}")
        print(f"users表中教师用户: {total_teacher_users}")
        print(f"teachers表中记录: {total_teachers}")

if __name__ == "__main__":
    sync_user_tables()
