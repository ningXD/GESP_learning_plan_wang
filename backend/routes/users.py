from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import User
from extensions import db
import bcrypt

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
    # 只返回role为teacher的用户，不包括admin用户
    teachers = User.query.filter(User.role == 'teacher').all()
    return jsonify({'success': True, 'data': [teacher.to_dict() for teacher in teachers]}), 200