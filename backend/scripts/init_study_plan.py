import sys
import os

# 添加父目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime
from extensions import db
from models.models import User, StudyPlan, StudyPlanWeek
import bcrypt

# 初始化学生账号和学习计划模板
def init_study_plan_template():
    try:
        # 检查学生账号是否存在
        student = User.query.filter_by(nickname='王乐汐').first()
        if not student:
            # 创建学生账号
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            student = User(
                username='wanglexi',
                password=hashed_password,
                nickname='王乐汐',
                role='student',
                admin=False,
                age=15,
                gender='女',
                grade='高一',
                subject='竞赛'
            )
            db.session.add(student)
            db.session.commit()
            print("学生账号 '王乐汐' 创建成功")
        else:
            print("学生账号 '王乐汐' 已存在")
        
        # 检查学习计划是否存在
        study_plan = StudyPlan.query.filter_by(student_id=student.id).first()
        if not study_plan:
            # 创建学习计划模板
            study_plan = StudyPlan(
                student_id=student.id,
                name='竞赛 8周冲刺计划表',
                start_date=datetime.strptime('2026-01-16', '%Y-%m-%d').date(),
                end_date=datetime.strptime('2026-03-13', '%Y-%m-%d').date(),
                description='每周五19:00-21:00学习，共8周的竞赛冲刺计划'
            )
            db.session.add(study_plan)
            db.session.commit()
            
            # 创建8周的学习计划
            weeks_data = [
                {
                    'week_number': 1,
                    'date': '2026-01-16',
                    'topic': '基础巩固与变量',
                    'core_knowledge': '1. 计算机基础（内存、网络、存储单位）\n2. 变量命名规则\n3. 数据类型与转换\n4. 输入输出（cin/cout）',
                    'practice': '<strong>真题：202309</strong> <a href="../materials/real_test_question_materials/202309.pdf" target="_blank" class="btn-small">查看真题</a>\n• 重点：选择题1-5，判断题1-5\n• 编程题1（X字矩阵）：理解双重循环与条件输出'
                },
                {
                    'week_number': 2,
                    'date': '2026-01-23',
                    'topic': '分支结构深入',
                    'core_knowledge': '1. if-else if-else 嵌套\n2. switch-case（注意break）\n3. 逻辑运算符（&&, ||, !）\n4. 流程图符号与解读',
                    'practice': '<strong>真题：202312</strong> <a href="../materials/real_test_question_materials/202312.pdf" target="_blank" class="btn-small">查看真题</a>\n• 重点：选择题3-8，判断题1-5\n• 编程题1（小杨做题）：理解循环与累加'
                },
                {
                    'week_number': 3,
                    'date': '2026-01-30',
                    'topic': '循环结构深入',
                    'core_knowledge': '1. for循环三要素\n2. while循环（先判断后执行）\n3. do-while循环（先执行后判断）\n4. break与continue区别',
                    'practice': '<strong>真题：202403</strong> <a href="../materials/real_test_question_materials/202403.pdf" target="_blank" class="btn-small">查看真题</a>\n• 重点：选择题6-10，判断题6-10\n• 编程题1（乘法问题）：注意数据范围与溢出判断'
                },
                {
                    'week_number': 4,
                    'date': '2026-02-06',
                    'topic': '循环嵌套与ASCII',
                    'core_knowledge': '1. 双重循环执行过程\n2. ASCII码（\'A\'=65, \'a\'=97, \'0\'=48）\n3. 字符与整数的转换\n4. 数位分离（%10, /10）',
                    'practice': '<strong>真题：202406</strong> <a href="../materials/real_test_question_materials/202406.pdf" target="_blank" class="btn-small">查看真题</a>\n• 重点：选择题7-12，判断题6-10\n• 编程题1（平方之和）：学习枚举思路'
                },
                {
                    'week_number': 5,
                    'date': '2026-02-13',
                    'topic': '数学函数与综合',
                    'core_knowledge': '1. 数学函数：abs(), sqrt(), max(), min()\n2. 质数判断算法\n3. 回文数判断（数字反转）\n4. 闰年判断规则',
                    'practice': '<strong>真题：202409</strong> <a href="../materials/real_test_question_materials/202409.pdf" target="_blank" class="btn-small">查看真题</a>\n• 重点：选择题8-13，判断题6-10\n• 编程题1（数位之和）：经典数位分离应用'
                },
                {
                    'week_number': 6,
                    'date': '2026-02-20',
                    'topic': '矩阵绘制专题',
                    'core_knowledge': '1. 矩阵绘制通用思路：双重循环+条件判断\n2. 常见矩阵：X字、H字、日字、N字矩阵\n3. 找规律：对角线、中间行、边界的判断',
                    'practice': '<strong>真题：202412</strong> <a href="../materials/real_test_question_materials/202412.pdf" target="_blank" class="btn-small">查看真题</a>\n• 重点：选择题11-15，编程题2\n• 编程题2（N字矩阵）：掌握矩阵绘制模板'
                },
                {
                    'week_number': 7,
                    'date': '2026-02-27',
                    'topic': '综合应用与模拟',
                    'core_knowledge': '1. 综合题型：数位问题、日期计算、数列规律\n2. 错误排查：常见逻辑错误与边界条件\n3. 限时解题技巧',
                    'practice': '<strong>真题：202503</strong> <a href="../materials/real_test_question_materials/202503.pdf" target="_blank" class="btn-small">查看真题</a>\n• 完整模拟（选择判断30分钟）\n• 编程题重点：日期计算（闰年、月份天数）'
                },
                {
                    'week_number': 8,
                    'date': '2026-03-06',
                    'topic': '考前冲刺与查漏',
                    'core_knowledge': '1. 复习所有错题集\n2. 重点回顾：数位分离、质数判断、矩阵绘制\n3. 快速解题技巧：代入法、排除法',
                    'practice': '<strong>真题：202506</strong> <a href="../materials/real_test_question_materials/202506.pdf" target="_blank" class="btn-small">查看真题</a>\n• 完整模拟（严格限时）\n• 分析错题，针对薄弱点专项练习'
                }
            ]
            
            for week_data in weeks_data:
                week = StudyPlanWeek(
                    plan_id=study_plan.id,
                    week_number=week_data['week_number'],
                    date=datetime.strptime(week_data['date'], '%Y-%m-%d').date(),
                    topic=week_data['topic'],
                    core_knowledge=week_data['core_knowledge'],
                    practice=week_data['practice']
                )
                db.session.add(week)
            
            db.session.commit()
            print("学习计划模板创建成功")
        else:
            print("学习计划已存在")
            
    except Exception as e:
        print(f"初始化学习计划模板时出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        init_study_plan_template()
