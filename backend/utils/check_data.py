from app import app
from models.models import User, Student, Teacher

with app.app_context():
    print('=== 用户数据 ===')
    users = User.query.all()
    print(f'总用户数: {len(users)}')
    for user in users:
        print(f'ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}, 角色: {user.role}')
    
    print('\n=== 学生数据 ===')
    students = Student.query.all()
    print(f'总学生数: {len(students)}')
    for student in students[:5]:  # 只显示前5个学生
        print(f'ID: {student.id}, 姓名: {student.name}, 电话: {student.phone}')
    
    print('\n=== 教师数据 ===')
    teachers = Teacher.query.all()
    print(f'总教师数: {len(teachers)}')
    for teacher in teachers[:5]:  # 只显示前5个教师
        print(f'ID: {teacher.id}, 姓名: {teacher.name}, 电话: {teacher.phone}')
