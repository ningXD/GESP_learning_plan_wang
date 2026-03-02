from flask import Blueprint, request, jsonify
from models.models import StudyPlan, StudyPlanWeek, User
from extensions import db
from datetime import datetime
from decorators import token_required

study_plan_bp = Blueprint('study_plan', __name__)

@study_plan_bp.route('/api/study-plans', methods=['GET'])
@token_required
def get_study_plans(user):
    
    if user.role == 'student':
        # 学生只能查看自己的学习计划
        plans = StudyPlan.query.filter_by(student_id=user.id).all()
    elif user.role == 'teacher' or user.admin:
        # 教师和管理员可以查看所有学习计划
        plans = StudyPlan.query.all()
    else:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify([plan.to_dict() for plan in plans])

@study_plan_bp.route('/api/study-plans/<int:plan_id>', methods=['GET'])
@token_required
def get_study_plan(user, plan_id):
    plan = StudyPlan.query.get(plan_id)
    
    if not plan:
        return jsonify({'error': 'Study plan not found'}), 404
    
    # 检查权限
    if user.role == 'student' and plan.student_id != user.id:
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify(plan.to_dict())

@study_plan_bp.route('/api/study-plans', methods=['POST'])
@token_required
def create_study_plan(user):
    
    # 只有教师和管理员可以创建学习计划
    if user.role != 'teacher' and not user.admin:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    student_id = data.get('student_id')
    
    # 验证学生是否存在
    student = User.query.filter_by(id=student_id, role='student').first()
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    new_plan = StudyPlan(
        student_id=student_id,
        name=data.get('name'),
        start_date=datetime.strptime(data.get('start_date'), '%Y-%m-%d').date(),
        end_date=datetime.strptime(data.get('end_date'), '%Y-%m-%d').date(),
        description=data.get('description')
    )
    
    db.session.add(new_plan)
    db.session.commit()
    
    # 创建计划周
    weeks = data.get('weeks', [])
    for week_data in weeks:
        new_week = StudyPlanWeek(
            plan_id=new_plan.id,
            week_number=week_data.get('week_number'),
            date=datetime.strptime(week_data.get('date'), '%Y-%m-%d').date(),
            topic=week_data.get('topic'),
            core_knowledge=week_data.get('core_knowledge'),
            practice=week_data.get('practice')
        )
        db.session.add(new_week)
    
    db.session.commit()
    
    return jsonify(new_plan.to_dict()), 201

@study_plan_bp.route('/api/study-plans/<int:plan_id>', methods=['PUT'])
@token_required
def update_study_plan(user, plan_id):
    plan = StudyPlan.query.get(plan_id)
    
    if not plan:
        return jsonify({'error': 'Study plan not found'}), 404
    
    # 只有教师和管理员可以更新学习计划
    if user.role != 'teacher' and not user.admin:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # 更新基本信息
    if 'name' in data:
        plan.name = data.get('name')
    if 'start_date' in data:
        plan.start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
    if 'end_date' in data:
        plan.end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
    if 'description' in data:
        plan.description = data.get('description')
    
    # 更新计划周
    if 'weeks' in data:
        # 删除旧的周计划
        StudyPlanWeek.query.filter_by(plan_id=plan_id).delete()
        
        # 创建新的周计划
        for week_data in data.get('weeks'):
            new_week = StudyPlanWeek(
                plan_id=plan_id,
                week_number=week_data.get('week_number'),
                date=datetime.strptime(week_data.get('date'), '%Y-%m-%d').date(),
                topic=week_data.get('topic'),
                core_knowledge=week_data.get('core_knowledge'),
                practice=week_data.get('practice')
            )
            db.session.add(new_week)
    
    db.session.commit()
    
    return jsonify(plan.to_dict())

@study_plan_bp.route('/api/study-plans/<int:plan_id>', methods=['DELETE'])
@token_required
def delete_study_plan(user, plan_id):
    plan = StudyPlan.query.get(plan_id)
    
    if not plan:
        return jsonify({'error': 'Study plan not found'}), 404
    
    # 只有教师和管理员可以删除学习计划
    if user.role != 'teacher' and not user.admin:
        return jsonify({'error': 'Unauthorized'}), 401
    
    db.session.delete(plan)
    db.session.commit()
    
    return jsonify({'message': 'Study plan deleted successfully'})

@study_plan_bp.route('/api/students', methods=['GET'])
@token_required
def get_students(user):
    
    # 只有教师和管理员可以查看学生列表
    if user.role != 'teacher' and not user.admin:
        return jsonify({'error': 'Unauthorized'}), 401
    
    students = User.query.filter_by(role='student').all()
    return jsonify([{
        'id': student.id,
        'username': student.username,
        'nickname': student.nickname,
        'email': student.email
    } for student in students])
