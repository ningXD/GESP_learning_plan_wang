import sys
import os

# 添加项目根目录到 Python 路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extensions import db
from models.models import User
from app import app

# 使用应用上下文
with app.app_context():
    try:
        # 检查数据库连接
        print("连接到数据库成功")
        
        # 检查 User 模型是否有 level 字段
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        columns = [column['name'] for column in inspector.get_columns('users')]
        
        if 'level' not in columns:
            # 使用 SQLAlchemy 的迁移功能添加字段
            from sqlalchemy import text
            db.session.execute(text("ALTER TABLE users ADD COLUMN level INTEGER DEFAULT 1"))
            print("添加 level 字段成功")
        else:
            print("level 字段已经存在")
        
        # 更新现有用户的 level 值
        # 学生账号为 1 级
        db.session.execute(text("UPDATE users SET level = 1 WHERE role = 'student'"))
        # 教师账号为 2 级
        db.session.execute(text("UPDATE users SET level = 2 WHERE role = 'teacher'"))
        # 管理员账号为 9 级
        db.session.execute(text("UPDATE users SET level = 9 WHERE role = 'admin'"))
        print("更新用户等级成功")
        
        db.session.commit()
        print("操作完成")
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        db.session.rollback()
