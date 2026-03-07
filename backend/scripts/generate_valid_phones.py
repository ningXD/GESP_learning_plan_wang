import sys
import os
import random

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app
from models.models import User, Student, Teacher
from extensions import db

def generate_valid_phone():
    """生成符合中国大陆格式的手机号码"""
    # 中国大陆手机号前缀
    prefixes = [
        '130', '131', '132', '133', '134', '135', '136', '137', '138', '139',
        '145', '146', '147', '148', '149',
        '150', '151', '152', '153', '155', '156', '157', '158', '159',
        '160', '161', '162', '163', '165', '166', '167', '168', '169',
        '170', '171', '172', '173', '175', '176', '177', '178',
        '180', '181', '182', '183', '184', '185', '186', '187', '188', '189',
        '190', '191', '192', '193', '195', '196', '197', '198', '199'
    ]
    
    # 随机选择一个前缀
    prefix = random.choice(prefixes)
    # 生成8位随机数字
    suffix = ''.join(random.choices('0123456789', k=8))
    # 组合成完整的手机号
    return f"{prefix}{suffix}"

def generate_valid_phones():
    """为所有表生成有效的手机号码"""
    with app.app_context():
        try:
            print("=== 生成有效手机号码 ===")
            
            # 为users表生成有效手机号
            print("\n1. 更新Users表:")
            users = User.query.all()
            user_updated = 0
            for user in users:
                new_phone = generate_valid_phone()
                # 确保手机号唯一
                while User.query.filter_by(phone=new_phone).first():
                    new_phone = generate_valid_phone()
                user.phone = new_phone
                user_updated += 1
            print(f"  已更新 {user_updated} 条记录")
            
            # 为students表生成有效手机号
            print("\n2. 更新Students表:")
            students = Student.query.all()
            student_updated = 0
            for student in students:
                new_phone = generate_valid_phone()
                # 确保手机号唯一
                while Student.query.filter_by(phone=new_phone).first():
                    new_phone = generate_valid_phone()
                student.phone = new_phone
                student_updated += 1
            print(f"  已更新 {student_updated} 条记录")
            
            # 为teachers表生成有效手机号
            print("\n3. 更新Teachers表:")
            teachers = Teacher.query.all()
            teacher_updated = 0
            for teacher in teachers:
                new_phone = generate_valid_phone()
                # 确保手机号唯一
                while Teacher.query.filter_by(phone=new_phone).first():
                    new_phone = generate_valid_phone()
                teacher.phone = new_phone
                teacher_updated += 1
            print(f"  已更新 {teacher_updated} 条记录")
            
            # 提交事务
            db.session.commit()
            print(f"\n操作完成: 共更新 {user_updated + student_updated + teacher_updated} 条记录")
            
        except Exception as e:
            db.session.rollback()
            print(f"错误: {e}")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    generate_valid_phones()