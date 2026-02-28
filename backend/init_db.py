from app import app, db
from models import User
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
        db.session.commit()
        print('默认用户创建成功: username=demo, password=123456')
    else:
        print('数据库中已有用户')
    
    print('数据库初始化完成')