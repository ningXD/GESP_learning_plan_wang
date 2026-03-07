from app import app
from models.models import User
from extensions import db

with app.app_context():
    # 测试与登录API相同的查询
    test_username = 'demo'
    print(f"测试查询用户: {test_username}")
    
    # 执行与登录API相同的查询
    user = User.query.filter((User.username == test_username) | (User.phone == test_username)).first()
    
    if user:
        print(f"找到用户: {user.username}, ID: {user.id}, 角色: {user.role}")
        print(f"用户信息: {user.to_dict()}")
    else:
        print("未找到用户")
    
    # 测试其他用户
    test_users = ['teacher_test', 'student_test', '13800138000']
    for test_user in test_users:
        print(f"\n测试查询: {test_user}")
        user = User.query.filter((User.username == test_user) | (User.phone == test_user)).first()
        if user:
            print(f"找到用户: {user.username}, ID: {user.id}, 角色: {user.role}")
        else:
            print("未找到用户")
