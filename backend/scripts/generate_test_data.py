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

# 生成测试数据
def generate_test_data():
    app = init_db()
    
    with app.app_context():
        print("开始生成测试数据...")
        
        # 生成教师数据
        print("生成教师数据...")
        base_phone = 10000000000
        
        # 检查是否已有教师数据
        existing_teachers = User.query.filter_by(role='teacher').count()
        print(f"现有教师数量: {existing_teachers}")
        
        # 生成100个教师
        for i in range(1, 101):
            # 检查是否已存在
            existing = User.query.filter_by(username=f'teacher{i}').first()
            if existing:
                print(f"教师 {i} 已存在，跳过...")
                continue
            
            # 生成密码
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # 创建教师
            teacher = User(
                username=f'teacher{i}',
                password=hashed_password,
                nickname=f'测试教师{i}',
                phone=str(base_phone + i - 1),
                role='teacher'
            )
            db.session.add(teacher)
            
            if i % 10 == 0:
                db.session.commit()
                print(f"已生成 {i} 个教师")
        
        db.session.commit()
        print("教师数据生成完成！")
        
        # 获取所有教师
        teachers = User.query.filter_by(role='teacher').all()
        teacher_count = len(teachers)
        print(f"可用教师数量: {teacher_count}")
        
        # 生成学生数据
        print("生成学生数据...")
        
        # 检查是否已有学生数据
        existing_students = Student.query.count()
        print(f"现有学生数量: {existing_students}")
        
        # 生成100个学生
        for i in range(1, 101):
            # 检查是否已存在
            existing = Student.query.filter_by(phone=str(base_phone + 100 + i - 1)).first()
            if existing:
                print(f"学生 {i} 已存在，跳过...")
                continue
            
            # 分配教师（轮询分配）
            teacher_index = (i - 1) % teacher_count
            teacher_id = teachers[teacher_index].id
            
            # 生成密码
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # 先在users表中创建用户
            user = User(
                username=f'student{i}',
                password=hashed_password,
                nickname=f'测试学生{i}',
                phone=str(base_phone + 100 + i - 1),
                role='student'
            )
            db.session.add(user)
            db.session.flush()  # 获取user.id
            
            # 然后在students表中创建学生记录
            student = Student(
                teacher_id=teacher_id,
                name=f'测试学生{i}',
                gender='男' if i % 2 == 0 else '女',
                age=10 + (i % 10),
                grade=f'{(i % 6) + 1}年级',
                project='竞赛',
                phone=str(base_phone + 100 + i - 1)
            )
            db.session.add(student)
            
            if i % 10 == 0:
                db.session.commit()
                print(f"已生成 {i} 个学生")
        
        db.session.commit()
        print("学生数据生成完成！")
        
        # 检查最终数据
        final_teachers = User.query.filter_by(role='teacher').count()
        final_students = Student.query.count()
        
        print(f"\n数据生成完成！")
        print(f"教师总数: {final_teachers}")
        print(f"学生总数: {final_students}")

if __name__ == "__main__":
    generate_test_data()
