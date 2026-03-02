from app import app, db
from models.models import User
import bcrypt

# 创建应用上下文
with app.app_context():
    # 检查是否已有学生账号
    student_user = User.query.filter_by(username='student').first()
    if not student_user:
        # 创建学生测试账号
        student_password = bcrypt.hashpw('student123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        student_user = User(
            username='student',
            password=student_password,
            email='student@example.com',
            role='student'
        )
        db.session.add(student_user)
        print('学生测试账号创建成功: username=student, password=student123')
    else:
        print('学生测试账号已存在')
    
    # 检查是否已有教师账号
    teacher_user = User.query.filter_by(username='teacher').first()
    if not teacher_user:
        # 创建教师测试账号
        teacher_password = bcrypt.hashpw('teacher123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        teacher_user = User(
            username='teacher',
            password=teacher_password,
            email='teacher@example.com',
            role='teacher'
        )
        db.session.add(teacher_user)
        print('教师测试账号创建成功: username=teacher, password=teacher123')
    else:
        print('教师测试账号已存在')
    
    # 提交更改
    db.session.commit()
    print('测试账号检查和创建完成')