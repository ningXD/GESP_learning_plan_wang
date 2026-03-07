from flask import Blueprint, request, jsonify
from models.models import User, Teacher
from extensions import db
import bcrypt
from pypinyin import lazy_pinyin
from decorators import token_required

# 创建蓝图
bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """获取当前用户信息"""
    return jsonify(current_user.to_dict()), 200

@bp.route('/me', methods=['PUT'])
@token_required
def update_current_user(current_user):
    """更新当前用户信息"""
    data = request.get_json()
    if 'email' in data:
        current_user.email = data['email']
    if 'nickname' in data:
        current_user.nickname = data['nickname']
    if 'password' in data:
        # 加密新密码
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        current_user.password = hashed_password
    
    # 同步更新学生表中的对应数据（如果用户是学生）
    if current_user.role == 'student':
        from models.models import Student
        student = Student.query.filter_by(name=current_user.nickname).first()
        if student:
            if 'nickname' in data:
                student.name = data['nickname']
            # 可以根据需要添加其他字段的同步更新
    
    db.session.commit()
    return jsonify(current_user.to_dict()), 200

@bp.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """获取指定用户信息"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(user.to_dict()), 200

@bp.route('/teachers', methods=['GET'])
@token_required
def get_teachers(current_user):
    """获取所有教师"""
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取排序参数
        sort = request.args.get('sort', '')
        order = request.args.get('order', 'asc')
        
        # 获取搜索参数
        keyword = request.args.get('keyword', '')
        
        # 从Teacher表查询
        query = Teacher.query
        
        # 执行搜索
        if keyword:
            # 获取搜索字段
            fields = request.args.get('fields', 'name,phone,gender,project').split(',')
            search_conditions = []
            
            if 'name' in fields:
                search_conditions.append(Teacher.name.like(f'%{keyword}%'))
            if 'phone' in fields:
                search_conditions.append(Teacher.phone.like(f'%{keyword}%'))
            if 'gender' in fields:
                search_conditions.append(Teacher.gender.like(f'%{keyword}%'))
            if 'project' in fields:
                search_conditions.append(Teacher.teaching_subject.like(f'%{keyword}%'))
            
            if search_conditions:
                query = query.filter(db.or_(*search_conditions))
        
        # 执行排序
        if sort == 'name':
            # 按姓名拼音排序，支持数字自然排序
            import re
            
            def natural_sort_key(s):
                # 将字符串分解为字母和数字部分
                parts = re.split(r'(\d+)', s)
                # 将数字部分转换为整数，字母部分转换为拼音
                key = []
                for part in parts:
                    if part.isdigit():
                        key.append(int(part))
                    else:
                        key.append(''.join(lazy_pinyin(part)))
                return key
            
            teachers = query.all()
            # 按自然排序
            teachers.sort(key=lambda t: natural_sort_key(t.name or ''), reverse=(order == 'desc'))
            # 手动分页
            total = len(teachers)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_teachers = teachers[start:end]
            total_pages = (total + per_page - 1) // per_page
            
            # 构建教师数据列表
            teacher_data = []
            for teacher in paginated_teachers:
                teacher_dict = teacher.to_dict()
                teacher_data.append(teacher_dict)
            
            return jsonify({
                'success': True, 
                'data': teacher_data,
                'total': total,
                'page': page,
                'per_page': per_page,
                'pages': total_pages
            }), 200
        
        # 默认分页（无排序）
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        teachers = pagination.items
        total = pagination.total
        
        # 构建教师数据列表
        teacher_data = []
        for teacher in teachers:
            teacher_dict = teacher.to_dict()
            teacher_data.append(teacher_dict)
        
        return jsonify({
            'success': True, 
            'data': teacher_data,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    except Exception as e:
        print(f"获取教师列表时出错: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/teachers/search', methods=['GET'])
@token_required
def search_teachers(current_user):
    """搜索教师"""
    try:
        # 获取搜索参数
        keyword = request.args.get('keyword', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 构建搜索查询
        query = Teacher.query
        if keyword:
            query = query.filter(db.or_(
                Teacher.name.like(f'%{keyword}%'),
                Teacher.teaching_subject.like(f'%{keyword}%')
            ))
        
        # 分页查询
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        teachers = pagination.items
        total = pagination.total
        
        # 构建教师数据列表
        teacher_data = []
        for teacher in teachers:
            teacher_dict = teacher.to_dict()
            teacher_data.append(teacher_dict)
        
        return jsonify({
            'success': True, 
            'data': teacher_data,
            'total': total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200
    except Exception as e:
        print(f"搜索教师时出错: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/teachers', methods=['POST'])
@token_required
def add_teacher(current_user):
    """添加教师用户"""
    # 只有管理员可以添加教师
    if current_user.role != 'admin':
        return jsonify({'error': '权限不足'}), 403
    
    data = request.get_json()
    if not data or 'phone' not in data or 'name' not in data:
        return jsonify({'error': '请提供教师信息'}), 400
    
    try:
        phone = data.get('phone')
        name = data.get('name')
        
        # 检查phone是否已存在
        existing_user = User.query.filter_by(phone=phone).first()
        if existing_user:
            return jsonify({'error': '手机号已存在'}), 400
        
        # 创建用户记录（密码默认为123456）
        hashed_password = bcrypt.hashpw('123456'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user = User(
            username=None,  # 不再自动生成账号
            password=hashed_password,
            phone=phone,
            nickname=name,
            role='teacher'
        )
        db.session.add(new_user)
        db.session.commit()
        
        # 创建教师记录
        new_teacher = Teacher(
            user_id=new_user.id,
            gender=data.get('gender') or '',
            age=data.get('age'),
            phone=phone,
            teaching_subject=data.get('teaching_subject') or ''
        )
        db.session.add(new_teacher)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'data': new_teacher.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/students/<int:student_id>', methods=['PUT'])
@token_required
def update_student(current_user):
    """更新学生信息"""
    # 只有管理员或教师可以更新学生信息
    if current_user.role not in ['admin', 'teacher']:
        return jsonify({'error': '权限不足'}), 403
    
    data = request.get_json()
    student_id = request.view_args.get('student_id')
    
    try:
        # 获取学生记录
        from models.models import Student
        student = Student.query.get(student_id)
        if not student:
            return jsonify({'error': '学生不存在'}), 404
        
        # 更新学生信息
        if 'name' in data:
            student.name = data['name']
        if 'gender' in data:
            student.gender = data['gender']
        if 'age' in data:
            student.age = data['age']
        if 'grade' in data:
            student.grade = data['grade']
        if 'phone' in data:
            student.phone = data['phone']
        
        # 同步更新用户表中的对应数据
        user = User.query.filter_by(nickname=student.name).first()
        if user and user.role == 'student':
            if 'name' in data:
                user.nickname = data['name']
            if 'phone' in data:
                user.phone = data['phone']
        
        db.session.commit()
        return jsonify({
            'success': True, 
            'data': student.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500