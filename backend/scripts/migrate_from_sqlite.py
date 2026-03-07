import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('config/.env')

# 导入SQLite数据库
import sqlite3

# 导入PostgreSQL数据库
from app import app
from extensions import db
from models.models import User, Note, Student, Teacher, ClassRecord, CourseRecord, StudyPlan, StudyPlanWeek

print("开始从SQLite数据库迁移数据到PostgreSQL...")

# 连接SQLite数据库
sqlite_conn = sqlite3.connect('instance/gesp_study_plan.db')
sqlite_cursor = sqlite_conn.cursor()

# 获取SQLite中的用户数据
print("正在读取SQLite数据库中的用户数据...")
sqlite_cursor.execute("SELECT * FROM users")
sqlite_users = sqlite_cursor.fetchall()

print(f"找到 {len(sqlite_users)} 个用户")

# 创建应用上下文
with app.app_context():
    # 检查PostgreSQL中的用户数据
    postgres_users = User.query.all()
    print(f"PostgreSQL中已有 {len(postgres_users)} 个用户")
    
    # 如果PostgreSQL中没有用户，则从SQLite迁移
    if len(postgres_users) == 0:
        print("正在从SQLite迁移用户数据到PostgreSQL...")
        
        for user in sqlite_users:
            # 检查用户是否已存在
            existing_user = User.query.filter_by(id=user[0]).first()
            if not existing_user:
                # 创建新用户
                new_user = User(
                    id=user[0],
                    username=user[1],
                    password=user[2],
                    email=user[3],
                    role=user[4],
                    created_at=user[5],
                    updated_at=user[6]
                )
                db.session.add(new_user)
                print(f"迁移用户: {user[1]}")
        
        # 提交更改
        db.session.commit()
        print("用户数据迁移完成！")
    else:
        print("PostgreSQL中已有用户数据，跳过迁移")

# 关闭SQLite连接
sqlite_conn.close()
print("数据迁移操作完成！")
