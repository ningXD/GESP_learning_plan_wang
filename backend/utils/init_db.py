import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# 连接到PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="123456",  # 默认密码
    host="localhost",
    port="5432"
)

# 设置自动提交
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

# 创建游标
cur = conn.cursor()

# 检查数据库是否存在
cur.execute("SELECT 1 FROM pg_database WHERE datname='gesp_study_plan'")
exists = cur.fetchone()

if not exists:
    # 创建数据库
    cur.execute("CREATE DATABASE gesp_study_plan")
    print("Database created successfully")
else:
    print("Database already exists")

# 检查用户是否存在
cur.execute("SELECT 1 FROM pg_roles WHERE rolname='gesp_user'")
user_exists = cur.fetchone()

if not user_exists:
    # 创建用户
    cur.execute("CREATE USER gesp_user WITH PASSWORD '123456'")
    print("User created successfully")
else:
    print("User already exists")

# 授予用户权限
cur.execute("GRANT ALL PRIVILEGES ON DATABASE gesp_study_plan TO gesp_user")
print("Database permissions granted successfully")

# 连接到gesp_study_plan数据库
conn.close()
conn = psycopg2.connect(
    dbname="gesp_study_plan",
    user="postgres",
    password="123456",
    host="localhost",
    port="5432"
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# 授予对public模式的权限
cur.execute("GRANT ALL PRIVILEGES ON SCHEMA public TO gesp_user")
print("Schema permissions granted successfully")

# 关闭连接
cur.close()
conn.close()
print("Database initialization completed")