from app import app
from extensions import db
from models.models import User
from datetime import datetime
import re

print("开始清理PostgreSQL中的现有用户...")

# 创建应用上下文
with app.app_context():
    # 删除所有用户
    User.query.delete()
    db.session.commit()
    print("已删除所有用户")

# 运行迁移脚本
print("\n开始从SQLite数据库迁移数据到PostgreSQL...")
import sqlite3

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
    # 从SQLite迁移用户数据到PostgreSQL
    print("正在从SQLite迁移用户数据到PostgreSQL...")
    
    success_count = 0
    error_count = 0
    
    for user in sqlite_users:
        try:
            # 提取用户数据
            user_id = user[0]
            username = user[1]
            password = user[2]
            email = user[3]
            
            # 处理role字段（从第5列开始）
            role = user[4] if len(user) > 4 else 'student'
            
            # 确保created_at和updated_at都是有效的时间戳
            created_at = datetime.now()
            updated_at = datetime.now()
            
            # 尝试处理时间字段，但如果失败则使用当前时间
            if len(user) > 5:
                try:
                    created_at_val = user[5]
                    if created_at_val:
                        if isinstance(created_at_val, str):
                            # 尝试解析字符串时间
                            if re.match(r'^\d+$', created_at_val):
                                # 数字时间戳
                                created_at = datetime.fromtimestamp(int(created_at_val))
                            elif created_at_val != 'admin':  # 排除无效值
                                created_at = datetime.fromisoformat(created_at_val)
                        elif isinstance(created_at_val, int):
                            # 整数时间戳
                            created_at = datetime.fromtimestamp(created_at_val)
                        else:
                            # 其他类型
                            created_at = datetime.now()
                except:
                    pass
            
            if len(user) > 6:
                try:
                    updated_at_val = user[6]
                    if updated_at_val:
                        if isinstance(updated_at_val, str):
                            # 尝试解析字符串时间
                            if re.match(r'^\d+$', updated_at_val):
                                # 数字时间戳
                                updated_at = datetime.fromtimestamp(int(updated_at_val))
                            else:
                                updated_at = datetime.fromisoformat(updated_at_val)
                        elif isinstance(updated_at_val, int):
                            # 整数时间戳
                            updated_at = datetime.fromtimestamp(updated_at_val)
                        else:
                            # 其他类型
                            updated_at = datetime.now()
                except:
                    pass
            
            # 创建新用户
            new_user = User(
                id=user_id,
                username=username,
                password=password,
                email=email,
                role=role,
                created_at=created_at,
                updated_at=updated_at
            )
            
            db.session.add(new_user)
            success_count += 1
            print(f"迁移用户: {username} (ID: {user_id})")
            
        except Exception as e:
            error_count += 1
            print(f"迁移用户失败 {user[1]}: {str(e)}")
            continue
    
    # 提交更改
    try:
        db.session.commit()
        print(f"用户数据迁移完成！成功: {success_count}, 失败: {error_count}")
    except Exception as e:
        print(f"提交更改失败: {str(e)}")
        # 尝试分批提交
        print("尝试分批提交...")
        db.session.rollback()
        
        # 重新开始，分批处理
        batch_size = 50
        total = len(sqlite_users)
        
        for i in range(0, total, batch_size):
            batch = sqlite_users[i:i+batch_size]
            print(f"处理批次 {i//batch_size + 1}/{(total + batch_size - 1)//batch_size}")
            
            try:
                for user in batch:
                    try:
                        # 提取用户数据
                        user_id = user[0]
                        username = user[1]
                        password = user[2]
                        email = user[3]
                        role = user[4] if len(user) > 4 else 'student'
                        
                        # 确保时间字段有效
                        created_at = datetime.now()
                        updated_at = datetime.now()
                        
                        # 创建新用户
                        new_user = User(
                            id=user_id,
                            username=username,
                            password=password,
                            email=email,
                            role=role,
                            created_at=created_at,
                            updated_at=updated_at
                        )
                        db.session.add(new_user)
                    except:
                        continue
                
                db.session.commit()
                print(f"批次 {i//batch_size + 1} 提交成功")
            except Exception as e:
                print(f"批次 {i//batch_size + 1} 提交失败: {str(e)}")
                db.session.rollback()
                continue

# 关闭SQLite连接
sqlite_conn.close()
print("数据迁移操作完成！")
