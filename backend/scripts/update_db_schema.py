#!/usr/bin/env python3
"""
更新数据库表结构，添加phone字段
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from extensions import db
from sqlalchemy import text

def update_db_schema():
    """更新数据库表结构"""
    with app.app_context():
        # 获取数据库连接
        conn = db.engine.connect()
        
        try:
            # 为users表添加phone字段
            print("正在为users表添加phone字段...")
            conn.execute(text("ALTER TABLE users ADD COLUMN phone TEXT"))
            print("users表添加phone字段成功")
        except Exception as e:
            print(f"users表添加phone字段失败: {e}")
        
        try:
            # 为students表添加phone字段
            print("正在为students表添加phone字段...")
            conn.execute(text("ALTER TABLE students ADD COLUMN phone TEXT NOT NULL DEFAULT ''"))
            print("students表添加phone字段成功")
        except Exception as e:
            print(f"students表添加phone字段失败: {e}")
        
        # 关闭连接
        conn.close()
        print("数据库表结构更新完成")

if __name__ == '__main__':
    update_db_schema()
