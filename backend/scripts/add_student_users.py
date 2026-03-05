import sys
import os
from datetime import datetime
import bcrypt

# 添加backend目录到路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 导入所需模块
from extensions import db
from models.models import User, Student

# 初始化数据库
def init_db():
    from app import app
    with app.app_context():
        return app

# 为现有学生添加用户账号
def add_student_users():
    app = init_db()
    
    with app.app_context():
        print("开始为现有学生添加用户账号...")
        
        # 获取所有学生
        students = Student.query.all()
        print(f"现有学生数量: {len(students)}")
        
        # 为每个学生创建用户账号
        added_count = 0
        for i, student in enumerate(students, 1):
            # 检查是否已有用户账号
            existing_user = User.query.filter_by(phone=student.phone).first()
            if existing_user:
                print(f"学生 {student.name} 已有用户账号，跳过...")
                continue
            
            # 生成密码
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # 创建用户账号
            user = User(
                username=f'student{i}',
                password=hashed_password,
                nickname=student.name,
                phone=student.phone,
                role='student',
                admin=False,
                age=student.age,
                gender=student.gender,
                grade=student.grade,
                subject=student.project
            )
            db.session.add(user)
            added_count += 1
            
            if added_count % 10 == 0:
                db.session.commit()
                print(f"已添加 {added_count} 个学生用户账号")
        
        db.session.commit()
        print(f"\n学生用户账号添加完成！")
        print(f"共添加 {added_count} 个学生用户账号")

if __name__ == "__main__":
    add_student_users()
