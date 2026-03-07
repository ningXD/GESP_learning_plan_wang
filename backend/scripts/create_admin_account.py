from app import app, db
from models.models import User
import bcrypt

# 创建应用上下文
with app.app_context():
    # 检查是否已有管理员账号
    admin_user = User.query.filter_by(username='demo').first()
    if not admin_user:
        # 创建管理员测试账号
        admin_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        admin_user = User(
            username='demo',
            password=admin_password,
            email='admin@example.com',
            role='admin'
        )
        db.session.add(admin_user)
        print('管理员测试账号创建成功: username=demo, password=123456')
    else:
        print('管理员测试账号已存在')
    
    # 提交更改
    db.session.commit()
    print('管理员账号检查和创建完成')
