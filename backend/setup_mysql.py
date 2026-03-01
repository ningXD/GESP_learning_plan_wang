import os
from dotenv import load_dotenv
import pymysql

# 加载环境变量
load_dotenv()

# 获取数据库配置
DATABASE_URL = os.getenv('DATABASE_URL')

# 解析数据库 URL
import urllib.parse
parsed_url = urllib.parse.urlparse(DATABASE_URL)
username = parsed_url.username
password = parsed_url.password
host = parsed_url.hostname
port = parsed_url.port or 3306
database = parsed_url.path[1:]  # 去掉开头的 '/' 字符

print(f"Connecting to MySQL: {username}@{host}:{port}/{database}")

try:
    # 连接到 MySQL 服务器
    connection = pymysql.connect(
        host=host,
        user=username,
        password=password,
        port=port,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    with connection.cursor() as cursor:
        # 创建数据库
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"Database {database} created successfully")
        
        # 选择数据库
        cursor.execute(f"USE {database}")
        
        # 创建用户表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("Users table created successfully")
        
        # 创建笔记表
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            content TEXT,
            type VARCHAR(20) NOT NULL,
            images JSON,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        ''')
        print("Notes table created successfully")
        
        # 检查是否已有演示用户
        cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'demo'")
        result = cursor.fetchone()
        
        if result['COUNT(*)'] == 0:
            # 创建演示用户
            import bcrypt
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)",
                ('demo', hashed_password, 'demo@example.com')
            )
            connection.commit()
            print("Demo user created successfully: username=demo, password=123456")
        else:
            print("Demo user already exists")
    
    print("MySQL setup completed successfully")
    
except Exception as e:
    print(f"Error: {e}")
finally:
    if 'connection' in locals() and connection.open:
        connection.close()