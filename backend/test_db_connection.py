import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

# 加载环境变量
load_dotenv('config/.env')

# 获取数据库URL
db_url = os.getenv('DATABASE_URL')

print(f"Testing database connection to: {db_url}")

try:
    # 创建数据库引擎
    engine = create_engine(db_url)
    
    # 测试连接
    with engine.connect() as conn:
        print("Database connection successful!")
        
        # 检查数据库是否存在
        if 'postgresql' in db_url:
            # 对于PostgreSQL，检查数据库是否存在
            print("PostgreSQL connection established.")
            
except OperationalError as e:
    print(f"Database connection failed: {e}")
    print("Please ensure PostgreSQL is running and the database exists.")

except Exception as e:
    print(f"Error: {e}")
