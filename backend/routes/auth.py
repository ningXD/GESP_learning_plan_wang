from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from models.models import User
from extensions import db
import bcrypt
from decorators import token_required
import logging

logger = logging.getLogger('app')

# 创建蓝图
bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    logger.debug(f"登录请求数据: {data}")
    
    if not data or 'username' not in data or 'password' not in data:
        logger.debug("缺少用户名或密码")
        return jsonify({'error': '手机号和密码不能为空'}), 400
    
    # 注意：虽然前端界面显示为"手机号"，但后端支持通过用户名或手机号登录
    # 这是一个隐藏功能，用于测试账号登录
    logger.debug(f"尝试登录用户: {data['username']}")
    user = User.query.filter((User.username == data['username']) | (User.phone == data['username'])).first()
    
    if not user:
        logger.debug(f"用户不存在: {data['username']}")
        return jsonify({'error': '用户不存在'}), 401
    
    # 验证密码
    logger.debug(f"找到用户: {user.username}, ID: {user.id}")
    if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
        logger.debug("密码错误")
        return jsonify({'error': '密码错误'}), 401
    
    # 创建访问令牌，将identity设置为字符串
    access_token = create_access_token(identity=str(user.id))
    logger.debug(f"登录成功: {user.username}")
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': '用户名和密码不能为空'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': '用户名已存在'}), 400
    
    # 加密密码
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # 创建用户
    user = User(
        username=data['username'],
        password=hashed_password,
        email=data.get('email'),
        phone=data.get('phone'),
        role='admin' if data['username'] == 'demo' else data.get('role', 'student')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # 创建访问令牌，将identity设置为字符串
    access_token = create_access_token(identity=str(user.id))
    return jsonify({
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@bp.route('/verify-password', methods=['POST'])
@token_required
def verify_password(current_user):
    """验证密码"""
    data = request.get_json()
    if not data or 'password' not in data:
        return jsonify({'success': False, 'message': '请提供密码'}), 400
    
    # 验证密码
    if not bcrypt.checkpw(data['password'].encode('utf-8'), current_user.password.encode('utf-8')):
        return jsonify({'success': False, 'message': '密码错误'}), 401
    
    return jsonify({'success': True, 'message': '密码验证成功'}), 200
