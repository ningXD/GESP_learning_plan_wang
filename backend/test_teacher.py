from models.models import db, User, Teacher

# 测试数据库连接和教师数据
def test_teachers():
    try:
        # 尝试获取所有教师
        teachers = User.query.filter(User.role == 'teacher').all()
        print(f"找到 {len(teachers)} 个教师")
        
        for teacher in teachers:
            print(f"教师: {teacher.username}, Nickname: {teacher.nickname}")
            # 检查是否有对应的Teacher记录
            if hasattr(teacher, 'teacher_profile') and teacher.teacher_profile:
                print(f"  Teacher记录: ID={teacher.teacher_profile.id}, Name={teacher.teacher_profile.name}")
            else:
                print("  没有对应的Teacher记录")
        
        print("测试成功")
    except Exception as e:
        print(f"测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_teachers()
