import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

# 加载环境变量
load_dotenv('config/.env')

# 获取数据库URL
db_url = os.getenv('DATABASE_URL')

print(f"Checking database tables in: {db_url}")

try:
    # 创建数据库引擎
    engine = create_engine(db_url)
    
    # 创建inspector来检查数据库结构
    inspector = inspect(engine)
    
    # 获取所有表名
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")
    
    # 检查每个表的列
    for table in tables:
        print(f"\nTable: {table}")
        columns = inspector.get_columns(table)
        for column in columns:
            print(f"  - {column['name']}: {column['type']}")
    
except Exception as e:
    print(f"Error: {e}")
