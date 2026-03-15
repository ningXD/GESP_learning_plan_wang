import sqlite3

# 连接到数据库
db_path = 'instance/gesp_study_plan.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# 检查 users 表是否已经有 level 字段
try:
    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]
    
    if 'level' not in columns:
        # 添加 level 字段，默认值为 1
        cursor.execute("ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1")
        print("添加 level 字段成功")
        
        # 更新现有用户的 level 值
        # 学生账号为 1 级
        cursor.execute("UPDATE users SET level = 1 WHERE role = 'student'")
        # 教师账号为 2 级
        cursor.execute("UPDATE users SET level = 2 WHERE role = 'teacher'")
        # 管理员账号为 9 级
        cursor.execute("UPDATE users SET level = 9 WHERE role = 'admin'")
        print("更新用户等级成功")
    else:
        print("level 字段已经存在")
        
    conn.commit()
except Exception as e:
    print(f"错误: {e}")
    conn.rollback()
finally:
    conn.close()
