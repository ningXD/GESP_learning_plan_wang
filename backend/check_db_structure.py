from app import app
from extensions import db

with app.app_context():
    print('=== 检查数据库结构 ===')
    
    # 获取所有表名
    inspector = db.inspect(db.engine)
    tables = inspector.get_table_names()
    
    print(f'数据库中的表: {tables}')
    
    # 检查users表结构
    if 'users' in tables:
        print('\n=== users表结构 ===')
        columns = inspector.get_columns('users')
        for column in columns:
            print(f"字段: {column['name']}, 类型: {column['type']}, 可空: {column['nullable']}")
    
    # 检查students表结构
    if 'students' in tables:
        print('\n=== students表结构 ===')
        columns = inspector.get_columns('students')
        for column in columns:
            print(f"字段: {column['name']}, 类型: {column['type']}, 可空: {column['nullable']}")
