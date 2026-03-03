import sys
import os

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

def check_db():
    app = init_db()
    
    with app.app_context():
        print("检查数据库表结构和数据...")
        
        # 检查用户表
        total_users = User.query.count()
        student_users = User.query.filter_by(role='student').count()
        teacher_users = User.query.filter_by(role='teacher').count()
        admin_users = User.query.filter_by(role='admin').count()
        
        print(f"\n用户表统计:")
        print(f"总用户数: {total_users}")
        print(f"学生用户: {student_users}")
        print(f"教师用户: {teacher_users}")
        print(f"管理员用户: {admin_users}")
        
        # 检查学生表
        total_students = Student.query.count()
        print(f"\n学生表统计:")
        print(f"总学生数: {total_students}")
        
        # 检查教师表
        total_teachers = Teacher.query.count()
        print(f"\n教师表统计:")
        print(f"总教师数: {total_teachers}")
        
        # 检查关联性
        print(f"\n关联性检查:")
        print(f"学生用户数与学生表记录数是否一致: {student_users == total_students}")
        print(f"教师用户数与教师表记录数是否一致: {teacher_users == total_teachers}")
        
        # 检查教师表的字段
        print(f"\n教师表字段检查:")
        if total_teachers > 0:
            teacher = Teacher.query.first()
            print(f"教师ID: {teacher.id}")
            print(f"用户ID: {teacher.user_id}")
            print(f"性别: {teacher.gender}")
            print(f"年龄: {teacher.age}")
            print(f"电话: {teacher.phone}")
            print(f"教学项目: {teacher.teaching_subject}")
        
        print("\n检查完成！")

if __name__ == "__main__":
    check_db()