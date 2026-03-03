from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, JWTManager
from models.models import User
import traceback


def token_required(f):
    """JWT token 认证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            # 打印请求头，检查Authorization头
            print(f"Request headers: {dict(request.headers)}")
            # 验证JWT token
            verify_jwt_in_request()
            # 获取当前用户ID
            user_id = get_jwt_identity()
            print(f"User ID from JWT: {user_id}")
            # 转换为整数
            try:
                user_id = int(user_id)
            except ValueError:
                print(f"Invalid user ID: {user_id}")
                return jsonify({'success': False, 'message': '认证失败'}), 401
            # 查询用户
            user = User.query.get(user_id)
            if not user:
                return jsonify({'success': False, 'message': '用户不存在'}), 404
            # 将用户对象传递给视图函数
            return f(user, *args, **kwargs)
        except Exception as e:
            print(f"认证错误: {e}")
            print(f"Traceback: {traceback.format_exc()}")
            return jsonify({'success': False, 'message': '认证失败'}), 401

    return decorated_function
