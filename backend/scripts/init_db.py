from app import app, db
from models.models import User
import bcrypt

# 创建应用上下文
with app.app_context():
    # 创建所有表
    db.create_all()
    
    # 检查是否已有用户
    if User.query.count() == 0:
        # 创建默认用户
        hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        demo_user = User(
            username='demo',
            password=hashed_password,
            email='demo@example.com'
        )
        db.session.add(demo_user)
        
        # 创建学生测试账号
        student_password = bcrypt.hashpw('student123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        student_user = User(
            username='student',
            password=student_password,
            email='student@example.com',
            role='student'
        )
        db.session.add(student_user)
        
        # 创建教师测试账号
        teacher_password = bcrypt.hashpw('teacher123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        teacher_user = User(
            username='teacher',
            password=teacher_password,
            email='teacher@example.com',
            role='teacher'
        )
        db.session.add(teacher_user)
        
        db.session.commit()
        print('默认用户创建成功: username=demo, password=123456')
        print('学生测试账号创建成功: username=student, password=student123')
        print('教师测试账号创建成功: username=teacher, password=teacher123')
    else:
        print('数据库中已有用户')
    
    print('数据库初始化完成')