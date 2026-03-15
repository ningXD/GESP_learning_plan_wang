from app import app
from models.models import User
from extensions import db
import bcrypt

with app.app_context():
    print('=== 创建账号 ===')
    
    # 创建管理账号
    admin_user = User.query.filter_by(username='demo').first()
    if not admin_user:
        hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = User(
            username='demo',
            password=hashed_password,
            nickname='管理员',
            phone='13800138000',
            role='admin'
        )
        db.session.add(admin_user)
        db.session.commit()
        print('管理账号创建成功: demo/123456')
    else:
        print('管理账号已存在: demo/123456')
    
    # 创建教师测试账号
    teacher_user = User.query.filter_by(username='teacher_test').first()
    if not teacher_user:
        hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        teacher_user = User(
            username='teacher_test',
            password=hashed_password,
            nickname='测试教师',
            phone='13800138001',
            role='teacher'
        )
        db.session.add(teacher_user)
        db.session.commit()
        print('教师账号创建成功: teacher_test/123456')
    else:
        print('教师账号已存在: teacher_test/123456')
    
    # 创建学生测试账号
    student_user = User.query.filter_by(username='student_test').first()
    if not student_user:
        hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        student_user = User(
            username='student_test',
            password=hashed_password,
            nickname='测试学生',
            phone='13800138002',
            role='student'
        )
        db.session.add(student_user)
        db.session.commit()
        print('学生账号创建成功: student_test/123456')
    else:
        print('学生账号已存在: student_test/123456')
    
    print('=== 账号创建完成 ===')
