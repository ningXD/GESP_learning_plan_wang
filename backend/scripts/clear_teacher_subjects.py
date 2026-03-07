import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from models.models import Teacher
from extensions import db

def clear_teacher_subjects():
    """清空teachers表里的所有科目字段"""
    with app.app_context():
        try:
            # 获取所有教师记录
            teachers = Teacher.query.all()
            print(f"找到 {len(teachers)} 个教师记录")
            
            # 清空每个教师的科目字段
            for teacher in teachers:
                teacher.teaching_subject = ''
            
            # 提交事务
            db.session.commit()
            print("操作完成: 已清空所有教师的科目字段")
            
        except Exception as e:
            db.session.rollback()
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    clear_teacher_subjects()