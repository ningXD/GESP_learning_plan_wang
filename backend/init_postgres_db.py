import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv('config/.env')

# 导入应用和数据库
from app import app
from extensions import db

# 导入所有模型，确保它们被注册
from models.models import User, Note, Student, Teacher, ClassRecord, CourseRecord, StudyPlan, StudyPlanWeek

print("Initializing PostgreSQL database...")

with app.app_context():
    # 创建所有表
    db.create_all()
    print("Database tables created successfully!")
    
    # 检查创建的表
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f"Created tables: {tables}")
