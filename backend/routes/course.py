from flask import Blueprint, request, jsonify
from models.models import Student, ClassRecord, CourseRecord, User
from extensions import db
from datetime import datetime
from decorators import token_required
import bcrypt
from pypinyin import lazy_pinyin

course_bp = Blueprint('course', __name__)

# 学员管理
@course_bp.route('/api/students', methods=['GET'])
@token_required
def get_students(current_user):
    # 只返回当前教师的学员，管理员可以看到所有学员
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以看到所有学生（User表中role为student的用户）
        students = User.query.filter_by(role='student').all()
    else:
        # 普通教师只能看到自己的学生
        students = Student.query.filter_by(teacher_id=current_user.id).all()
    
    return jsonify({'success': True, 'data': [student.to_dict() for student in students]}), 200

@course_bp.route('/api/students/<int:student_id>', methods=['GET'])
@token_required
def get_student(current_user, student_id):
    # 获取单个学员信息
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以查看所有学生
        # 先检查是否是Student表中的学生
        student = Student.query.get(student_id)
        if not student:
            # 检查是否是User表中的学生
            user = User.query.filter_by(id=student_id, role='student').first()
            if not user:
                return jsonify({'success': False, 'message': '学员不存在'}), 404
            return jsonify({'success': True, 'data': user.to_dict()}), 200
    else:
        # 普通教师只能查看自己的学生
        student = Student.query.filter_by(id=student_id, teacher_id=current_user.id).first()
        if not student:
            return jsonify({'success': False, 'message': '学员不存在或不属于您'}), 404
    
    return jsonify({'success': True, 'data': student.to_dict()}), 200

@course_bp.route('/api/students', methods=['POST'])
@token_required
def add_student(current_user):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请提供学员信息'}), 400
    
    try:
        # 生成用户名：根据学员姓名的拼音
        name = data.get('name')
        pinyin = ''.join(lazy_pinyin(name)).lower()
        
        # 检查用户名是否已存在
        existing_user = User.query.filter_by(username=pinyin).first()
        if not existing_user:
            # 创建新用户
            hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            new_user = User(
                username=pinyin,
                password=hashed_password,
                nickname=name,
                role='student',
                admin=False,
                age=data.get('age'),
                gender=data.get('gender'),
                grade=data.get('grade'),
                subject=data.get('project')
            )
            db.session.add(new_user)
            db.session.commit()
        
        # 创建学员记录
        new_student = Student(
            teacher_id=current_user.id,
            name=data.get('name'),
            gender=data.get('gender') or '',
            age=data.get('age'),
            grade=data.get('grade') or '',
            project=data.get('project') or ''
        )
        db.session.add(new_student)
        db.session.commit()
        return jsonify({'success': True, 'data': new_student.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@course_bp.route('/api/students/<int:student_id>', methods=['PUT'])
@token_required
def update_student(current_user, student_id):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以更新所有学生
        student = Student.query.get(student_id)
        if not student:
            # 检查是否是User表中的学生
            user = User.query.filter_by(id=student_id, role='student').first()
            if not user:
                return jsonify({'success': False, 'message': '学员不存在'}), 404
            # 为User表中的学生创建Student记录
            student = Student(
                teacher_id=current_user.id,
                name=user.nickname or user.username,
                gender=user.gender or '',
                age=user.age or 0,
                grade=user.grade or '',
                project=user.subject or ''
            )
            db.session.add(student)
            db.session.commit()
    else:
        # 普通教师只能更新自己的学生
        student = Student.query.filter_by(id=student_id, teacher_id=current_user.id).first()
    
    if not student:
        return jsonify({'success': False, 'message': '学员不存在或不属于您'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请提供更新信息'}), 400
    
    try:
        if 'name' in data:
            student.name = data['name']
        if 'gender' in data:
            student.gender = data['gender']
        if 'age' in data:
            student.age = data['age']
        if 'grade' in data:
            student.grade = data['grade']
        if 'project' in data:
            student.project = data['project']
        
        db.session.commit()
        return jsonify({'success': True, 'data': student.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@course_bp.route('/api/students/<int:student_id>', methods=['DELETE'])
@token_required
def delete_student(current_user, student_id):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以删除所有学生
        student = Student.query.get(student_id)
        if not student:
            # 检查是否是User表中的学生
            user = User.query.filter_by(id=student_id, role='student').first()
            if not user:
                return jsonify({'success': False, 'message': '学员不存在'}), 404
            # 为User表中的学生创建Student记录
            student = Student(
                teacher_id=current_user.id,
                name=user.nickname or user.username,
                gender=user.gender or '',
                age=user.age or 0,
                grade=user.grade or '',
                project=user.subject or ''
            )
            db.session.add(student)
            db.session.commit()
    else:
        # 普通教师只能删除自己的学生
        student = Student.query.filter_by(id=student_id, teacher_id=current_user.id).first()
    
    if not student:
        return jsonify({'success': False, 'message': '学员不存在或不属于您'}), 404
    
    try:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'success': True, 'message': '学员删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# 课程记录管理
@course_bp.route('/api/class-records', methods=['GET'])
@token_required
def get_class_records(current_user):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以看到所有课程记录
        class_records = ClassRecord.query.all()
    else:
        # 普通教师只能看到自己的课程记录
        class_records = ClassRecord.query.filter_by(teacher_id=current_user.id).all()
    
    return jsonify({'success': True, 'data': [record.to_dict() for record in class_records]}), 200

@course_bp.route('/api/class-records', methods=['POST'])
@token_required
def add_class_record(current_user):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请提供课程信息'}), 400
    
    try:
        # 验证学员是否存在（管理员可以为任何学生添加课程记录）
        if current_user.admin:
            # 管理员可以为User表中的学生或Student表中的学生添加课程记录
            student = Student.query.get(data.get('student_id'))
            if not student:
                # 检查是否是User表中的学生
                user = User.query.filter_by(id=data.get('student_id'), role='student').first()
                if not user:
                    return jsonify({'success': False, 'message': '学员不存在'}), 404
                # 为User表中的学生创建Student记录
                student = Student(
                    teacher_id=current_user.id,
                    name=user.nickname or user.username,
                    gender=user.gender or '',
                    age=user.age or 0,
                    grade=user.grade or '',
                    project=user.subject or ''
                )
                db.session.add(student)
                db.session.commit()
        else:
            # 普通教师只能为自己的学生添加课程记录
            student = Student.query.filter_by(id=data.get('student_id'), teacher_id=current_user.id).first()
        
        if not student:
            return jsonify({'success': False, 'message': '学员不存在或不属于您'}), 404
        
        new_class = ClassRecord(
            student_id=student.id,
            teacher_id=current_user.id,
            date=datetime.strptime(data.get('date'), '%Y-%m-%d').date(),
            start_time=datetime.strptime(data.get('start_time'), '%H:%M').time(),
            end_time=datetime.strptime(data.get('end_time'), '%H:%M').time(),
            topic=data.get('topic'),
            content=data.get('content')
        )
        db.session.add(new_class)
        db.session.commit()
        
        # 自动创建消课记录
        new_course_record = CourseRecord(
            class_id=new_class.id,
            student_id=data.get('student_id'),
            status='completed'
        )
        db.session.add(new_course_record)
        db.session.commit()
        
        return jsonify({'success': True, 'data': new_class.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@course_bp.route('/api/class-records/<int:class_id>', methods=['PUT'])
@token_required
def update_class_record(current_user, class_id):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以更新所有课程记录
        class_record = ClassRecord.query.get(class_id)
    else:
        # 普通教师只能更新自己的课程记录
        class_record = ClassRecord.query.filter_by(id=class_id, teacher_id=current_user.id).first()
    
    if not class_record:
        return jsonify({'success': False, 'message': '课程记录不存在'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请提供更新信息'}), 400
    
    try:
        if 'date' in data:
            class_record.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'start_time' in data:
            class_record.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            class_record.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        if 'topic' in data:
            class_record.topic = data['topic']
        if 'content' in data:
            class_record.content = data['content']
        
        db.session.commit()
        return jsonify({'success': True, 'data': class_record.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@course_bp.route('/api/class-records/<int:class_id>', methods=['DELETE'])
@token_required
def delete_class_record(current_user, class_id):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    if current_user.admin:
        # 管理员可以删除所有课程记录
        class_record = ClassRecord.query.get(class_id)
    else:
        # 普通教师只能删除自己的课程记录
        class_record = ClassRecord.query.filter_by(id=class_id, teacher_id=current_user.id).first()
    
    if not class_record:
        return jsonify({'success': False, 'message': '课程记录不存在'}), 404
    
    try:
        # 删除关联的消课记录
        course_records = CourseRecord.query.filter_by(class_id=class_id).all()
        for record in course_records:
            db.session.delete(record)
        
        db.session.delete(class_record)
        db.session.commit()
        return jsonify({'success': True, 'message': '课程记录删除成功'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# 消课记录管理
@course_bp.route('/api/course-records', methods=['GET'])
@token_required
def get_course_records(current_user):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    # 获取消课记录
    course_records = []
    if current_user.admin:
        # 管理员可以看到所有消课记录
        course_records = CourseRecord.query.all()
    else:
        # 普通教师只能看到自己的消课记录
        class_records = ClassRecord.query.filter_by(teacher_id=current_user.id).all()
        for class_record in class_records:
            records = CourseRecord.query.filter_by(class_id=class_record.id).all()
            course_records.extend(records)
    
    return jsonify({'success': True, 'data': [record.to_dict() for record in course_records]}), 200

@course_bp.route('/api/course-records/<int:record_id>', methods=['PUT'])
@token_required
def update_course_record(current_user, record_id):
    if current_user.role != 'teacher' and not current_user.admin:
        return jsonify({'success': False, 'message': '权限不足'}), 403
    
    course_record = CourseRecord.query.get(record_id)
    if not course_record:
        return jsonify({'success': False, 'message': '消课记录不存在'}), 404
    
    # 验证课程记录是否属于当前教师（非管理员）
    if not current_user.admin:
        class_record = ClassRecord.query.filter_by(id=course_record.class_id, teacher_id=current_user.id).first()
        if not class_record:
            return jsonify({'success': False, 'message': '无权操作此记录'}), 403
    
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '请提供更新信息'}), 400
    
    try:
        if 'status' in data:
            course_record.status = data['status']
        if 'notes' in data:
            course_record.notes = data['notes']
        
        db.session.commit()
        return jsonify({'success': True, 'data': course_record.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
