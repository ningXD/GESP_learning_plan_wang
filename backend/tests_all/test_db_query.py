from app import app
from models.models import User

with app.app_context():
    print('=== 测试数据库查询 ===')
    
    # 测试通过用户名查询
    print('\n=== 通过用户名查询 ===')
    demo_user = User.query.filter_by(username='demo').first()
    print(f"demo用户: {demo_user}")
    if demo_user:
        print(f"demo用户ID: {demo_user.id}")
    
    # 测试通过手机号查询
    print('\n=== 通过手机号查询 ===')
    phone_user = User.query.filter_by(phone='13800138000').first()
    print(f"手机号用户: {phone_user}")
    if phone_user:
        print(f"手机号用户ID: {phone_user.id}")
    
    # 测试使用OR条件查询
    print('\n=== 使用OR条件查询 ===')
    or_user = User.query.filter((User.username == 'demo') | (User.phone == 'demo')).first()
    print(f"OR条件查询结果: {or_user}")
    if or_user:
        print(f"OR条件查询用户ID: {or_user.id}")
