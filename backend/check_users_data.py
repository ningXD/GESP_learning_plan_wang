from app import app
from models.models import User

with app.app_context():
    print('=== 检查用户数据 ===')
    users = User.query.all()
    print(f'总用户数: {len(users)}')
    for user in users:
        print(f'ID: {user.id}, 用户名: {user.username}, 昵称: {user.nickname}, 角色: {user.role}, 电话: {user.phone}')
