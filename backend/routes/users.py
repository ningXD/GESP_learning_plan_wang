from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User, Teacher
from extensions import db
import bcrypt
from pypinyin import lazy_pinyin

# 创建蓝图
bp = Blueprint('users', __name__, url_prefix='/api/users')

@bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """获取当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(user.to_dict()), 200

@bp.route('/me', methods=['PUT'])
@jwt_required()
def update_current_user():
    """更新当前用户信息"""
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    
    data = request.get_json()
    if 'email' in data:
        user.email = data['email']
    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'password' in data:
        # 加密新密码
        hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        user.password = hashed_password
    
    db.session.commit()
    return jsonify(user.to_dict()), 200

@bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """获取指定用户信息"""
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': '用户不存在'}), 404
    return jsonify(user.to_dict()), 200

@bp.route('/teachers', methods=['GET'])
@jwt_required()
def get_teachers():
    """获取所有教师用户"""
    try:
        # 获取分页参数
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 获取排序参数
        sort = request.args.get('sort', '')
        order = request.args.get('order', 'asc')
        
        # 获取搜索参数
        keyword = request.args.get('keyword', '')
        
        # 只返回role为teacher的用户，不包括admin用户
        query = User.query.filter(User.role == 'teacher')
        
        # 执行搜索
        if keyword:
            # 获取搜索字段
            fields = request.args.get('fields', 'name,phone,gender,project,teacher').split(',')
            search_conditions = []
            
            if 'name' in fields:
                search_conditions.append(db.or_(
                    User.nickname.like(f'%{keyword}%'),
                    User.username.like(f'%{keyword}%')
                ))
            if 'phone' in fields:
                search_conditions.append(User.phone.like(f'%{keyword}%'))
            if 'gender' in fields:
                search_conditions.append(User.gender.like(f'%{keyword}%'))
            if 'project' in fields or 'subject' in fields:
                search_conditions.append(User.subject.like(f'%{keyword}%'))
            
            if search_conditions:
                query = query.filter(db.or_(*search_conditions))
        
        # 执行排序
        if sort == 'name':
            # 按姓名拼音排序
            teachers = query.all()
            # 按拼音排序
            teachers.sort(key=lambda t: ''.join(lazy_pinyin(t.nickname or t.username or '')), reverse=(order == 'desc'))
            # 手动分页
            total = len(teachers)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_teachers = teachers[start:end]
            total_pages = (total + per_page - 1) // per_page
            
            # 构建教师数据列表，使用User表中的nickname字段
            teacher_data = []
            for teacher in paginated_teachers:
                teacher_dict = teacher.to_dict()
                # 直接使用User表中的nickname字段
                teacher_dict['name'] = teacher_dict.get('nickname', '')
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
        
        # 构建教师数据列表，使用User表中的nickname字段
        teacher_data = []
        for teacher in teachers:
            teacher_dict = teacher.to_dict()
            # 直接使用User表中的nickname字段
            teacher_dict['name'] = teacher_dict.get('nickname', '')
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
@jwt_required()
def search_teachers():
    """搜索教师"""
    try:
        # 获取搜索参数
        keyword = request.args.get('keyword', '')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # 构建搜索查询
        query = User.query.filter(User.role == 'teacher')
        if keyword:
            query = query.filter(User.nickname.like(f'%{keyword}%'))
        
        # 分页查询
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        teachers = pagination.items
        total = pagination.total
        
        # 构建教师数据列表
        teacher_data = []
        for teacher in teachers:
            teacher_dict = teacher.to_dict()
            teacher_dict['name'] = teacher_dict.get('nickname', '')
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
@jwt_required()
def add_teacher():
    """添加教师用户"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)
    
    # 只有管理员可以添加教师
    if not current_user.admin:
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
            role='teacher',
            gender=data.get('gender') or '',
            age=data.get('age'),
            subject=data.get('teaching_subject') or ''
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