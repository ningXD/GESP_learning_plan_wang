from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from models.models import User


def token_required(f):
    """JWT token 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 验证JWT token，明确指定从headers获取
            verify_jwt_in_request(locations=['headers'])
            # 获取当前用户ID
            user_id = get_jwt_identity()
            # 查询用户
            user = User.query.get(user_id)
            if not user:
                return jsonify({'success': False, 'message': '用户不存在'}), 404
            # 将用户对象传递给视图函数
            return f(user, *args, **kwargs)
        except Exception as e:
            return jsonify({'success': False, 'message': '认证失败'}), 401

    return decorated_function
