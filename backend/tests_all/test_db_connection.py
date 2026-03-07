from app import app
from extensions import db
from models.models import User

with app.app_context():
    print(f"数据库URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"数据库连接状态: {'Connected' if db.engine.pool.size() > 0 else 'Not connected'}")
    
    # 检查当前数据库中的用户
    users = User.query.all()
    print(f"当前数据库中的用户数量: {len(users)}")
    for user in users:
        print(f"ID: {user.id}, 用户名: {user.username}, 电话: {user.phone}, 角色: {user.role}")
