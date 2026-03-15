from app import app
from models.models import User, Student, Teacher
from extensions import db

with app.app_context():
    print('=== 检查数据同步情况 ===')
    
    # 检查users表
    print('\n1. Users表数据:')
    users = User.query.all()
    for user in users:
        print(f"ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}, 角色: {user.role}, 电话: {user.phone}")
    
    # 检查students表
    print('\n2. Students表数据:')
    students = Student.query.all()
    for student in students:
        print(f"ID: {student.id}, 姓名: {student.name}, 电话: {student.phone}, 教师ID: {student.teacher_id}")
    
    # 检查teachers表
    print('\n3. Teachers表数据:')
    teachers = Teacher.query.all()
    for teacher in teachers:
        print(f"ID: {teacher.id}, 用户ID: {teacher.user_id}, 姓名: {teacher.name}, 电话: {teacher.phone}")
    
    # 检查数据同步情况
    print('\n4. 数据同步检查:')
    
    # 检查users表中的学生是否在students表中
    student_users = User.query.filter_by(role='student').all()
    print(f"\nUsers表中的学生数量: {len(student_users)}")
    print("Users表中的学生在Students表中的情况:")
    for user in student_users:
        student = Student.query.filter_by(name=user.nickname).first()
        if student:
            print(f"✓ 用户 {user.username} (昵称: {user.nickname}) 在Students表中存在")
        else:
            print(f"✗ 用户 {user.username} (昵称: {user.nickname}) 在Students表中不存在")
    
    # 检查users表中的教师是否在teachers表中
    teacher_users = User.query.filter_by(role='teacher').all()
    print(f"\nUsers表中的教师数量: {len(teacher_users)}")
    print("Users表中的教师在Teachers表中的情况:")
    for user in teacher_users:
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        if teacher:
            print(f"✓ 用户 {user.username} (ID: {user.id}) 在Teachers表中存在")
        else:
            print(f"✗ 用户 {user.username} (ID: {user.id}) 在Teachers表中不存在")
    
    # 检查students表中的学生是否在users表中
    print(f"\nStudents表中的学生数量: {len(students)}")
    print("Students表中的学生在Users表中的情况:")
    for student in students:
        user = User.query.filter_by(nickname=student.name, role='student').first()
        if user:
            print(f"✓ 学生 {student.name} 在Users表中存在")
        else:
            print(f"✗ 学生 {student.name} 在Users表中不存在")
