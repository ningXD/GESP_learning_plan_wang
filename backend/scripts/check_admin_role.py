from app import app
from extensions import db
from models.models import User

print("检查管理员用户的权限...")

# 创建应用上下文
with app.app_context():
    # 查询所有用户
    users = User.query.all()
    print(f"总用户数: {len(users)}")
    
    # 检查demo用户
    demo_user = User.query.filter_by(username='demo').first()
    if demo_user:
        print(f"\ndemo用户信息:")
        print(f"  ID: {demo_user.id}")
        print(f"  用户名: {demo_user.username}")
        print(f"  角色: {demo_user.role}")
        print(f"  邮箱: {demo_user.email}")
    else:
        print("\ndemo用户不存在！")
    
    # 检查其他管理员用户
    admin_users = User.query.filter_by(role='admin').all()
    print(f"\n管理员用户数量: {len(admin_users)}")
    for user in admin_users:
        print(f"  - {user.username