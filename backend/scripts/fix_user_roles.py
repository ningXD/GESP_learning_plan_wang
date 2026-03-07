from app import app
from extensions import db
from models.models import User

print("开始修复用户角色...")

# 创建应用上下文
with app.app_context():
    # 更新demo用户为管理员
    demo_user = User.query.filter_by(username='demo').first()
    if demo_user:
        demo_user.role = 'admin'
        print("已将demo用户设置为管理员")
    
    # 更新teacher_test用户为教师
    teacher_test = User.query.filter_by(username='teacher_test').first()
    if teacher_test:
        teacher_test.role = 'teacher'
        print("已将teacher_test用户设置为教师")
    
    # 更新所有teacher1-teacher100用户为教师
    for i in range(1, 101):
        teacher_user = User.query.filter_by(username=f'teacher{i}').first()
        if teacher_user:
            teacher_user.role = 'teacher'
    print("已将所有teacher1-teacher100用户设置为教师")
    
    # 更新所有student用户为学生
    student_test = User.query.filter_by(username='student_test').first()
    if student_test:
        student_test.role = 'student'
    
    for i in range(2, 102):
        student_user = User.query.filter_by(username=f'student{i}').first()
        if student_user:
            student_user.role = 'student'
    print("已将所有student用户设置为学生")
    
    # 提交更改
    db.session.commit()
    print("角色更新完成！")
    
    # 验证更新结果
    print("\n验证更新结果:")
    
    # 检查demo用户
    demo_user = User.query.filter_by(username='demo').first()
    if demo_user:
        print(f"demo用户角色: {demo_user.role}")
    
    # 检查管理员用户
    admin_users = User.query.filter_by(role='admin').all()
    print(f"管理员用户数量: {len(admin_users)}")
    
    # 检查教师用户
    teacher_users = User.query.filter_by(role='teacher').all()
    print(f"教师用户数量: {len(teacher_users)}")
    
    # 检查学生用户
    student_users = User.query.filter_by(role='student').all()
    print(f"学生用户数量: {len(student_users)}")

print("用户角色修复完成！")
