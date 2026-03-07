from app import app
from models.models import User, Student, Teacher
from extensions import db

with app.app_context():
    print('=== 修复数据同步 ===')
    
    # 1. 将Users表中的学生添加到Students表
    print('\n1. 将Users表中的学生添加到Students表:')
    student_users = User.query.filter_by(role='student').all()
    for user in student_users:
        # 检查是否已存在
        existing_student = Student.query.filter_by(name=user.nickname).first()
        if not existing_student:
            # 创建学生记录
            student = Student(
                teacher_id=1,  # 默认教师ID为1（管理员）
                name=user.nickname,
                phone=user.phone,
                age=15,  # 随机年龄
                grade='高一'  # 默认年级
            )
            db.session.add(student)
            print(f"✓ 添加学生: {user.nickname} (用户: {user.username})")
        else:
            print(f"✓ 学生 {user.nickname} 已存在")
    
    # 2. 将Users表中的教师添加到Teachers表
    print('\n2. 将Users表中的教师添加到Teachers表:')
    teacher_users = User.query.filter_by(role='teacher').all()
    for user in teacher_users:
        # 检查是否已存在
        existing_teacher = Teacher.query.filter_by(user_id=user.id).first()
        if not existing_teacher:
            # 创建教师记录
            teacher = Teacher(
                user_id=user.id,
                name=user.nickname,
                phone=user.phone
            )
            db.session.add(teacher)
            print(f"✓ 添加教师: {user.nickname} (用户: {user.username})")
        else:
            print(f"✓ 教师 {user.nickname} 已存在")
    
    # 3. 检查Students表中的学生是否在Users表中，如不存在则更新或删除
    print('\n3. 检查Students表中的学生:')
    students = Student.query.all()
    for student in students:
        user = User.query.filter_by(nickname=student.name, role='student').first()
        if not user:
            # 检查是否有匹配的用户（可能是昵称被更新了）
            user_by_phone = User.query.filter_by(phone=student.phone, role='student').first()
            if user_by_phone:
                # 更新学生姓名为用户昵称
                student.name = user_by_phone.nickname
                print(f"✓ 更新学生姓名: {student.name} (匹配电话: {student.phone})")
            else:
                # 删除不存在的学生记录
                db.session.delete(student)
                print(f"✗ 删除不存在的学生: {student.name}")
        else:
            # 同步电话
            if student.phone != user.phone:
                student.phone = user.phone
                print(f"✓ 同步学生电话: {student.name} -> {user.phone}")
    
    # 提交更改
    db.session.commit()
    print('\n=== 数据同步修复完成 ===')
    
    # 再次检查同步情况
    print('\n=== 同步后检查 ===')
    
    # 检查users表中的学生
    student_users = User.query.filter_by(role='student').all()
    print(f"Users表中的学生数量: {len(student_users)}")
    for user in student_users:
        student = Student.query.filter_by(name=user.nickname).first()
        status = "✓" if student else "✗"
        print(f"{status} 用户 {user.username} (昵称: {user.nickname}) 在Students表中{'存在' if student else '不存在'}")
    
    # 检查users表中的教师
    teacher_users = User.query.filter_by(role='teacher').all()
    print(f"\nUsers表中的教师数量: {len(teacher_users)}")
    for user in teacher_users:
        teacher = Teacher.query.filter_by(user_id=user.id).first()
        status = "✓" if teacher else "✗"
        print(f"{status} 用户 {user.username} (ID: {user.id}) 在Teachers表中{'存在' if teacher else '不存在'}")
