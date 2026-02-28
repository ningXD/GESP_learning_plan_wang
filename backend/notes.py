from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Note
from app import db, app
import os
import uuid

# 创建蓝图
bp = Blueprint('notes', __name__, url_prefix='/api/notes')

@bp.route('/', methods=['GET'])
@jwt_required()
def get_notes():
    """获取用户的所有笔记"""
    user_id = get_jwt_identity()
    notes = Note.query.filter_by(user_id=user_id).order_by(Note.created_at.desc()).all()
    return jsonify([note.to_dict() for note in notes]), 200

@bp.route('/<int:note_id>', methods=['GET'])
@jwt_required()
def get_note(note_id):
    """获取单个笔记"""
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': '笔记不存在'}), 404
    return jsonify(note.to_dict()), 200

@bp.route('/', methods=['POST'])
@jwt_required()
def create_note():
    """创建笔记"""
    user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or 'title' not in data or 'type' not in data:
        return jsonify({'error': '标题和类型不能为空'}), 400
    
    note = Note(
        user_id=user_id,
        title=data['title'],
        content=data.get('content'),
        type=data['type'],
        images=data.get('images')
    )
    
    db.session.add(note)
    db.session.commit()
    return jsonify(note.to_dict()), 201

@bp.route('/<int:note_id>', methods=['PUT'])
@jwt_required()
def update_note(note_id):
    """更新笔记"""
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': '笔记不存在'}), 404
    
    data = request.get_json()
    if 'title' in data:
        note.title = data['title']
    if 'content' in data:
        note.content = data['content']
    if 'type' in data:
        note.type = data['type']
    if 'images' in data:
        note.images = data['images']
    
    db.session.commit()
    return jsonify(note.to_dict()), 200

@bp.route('/<int:note_id>', methods=['DELETE'])
@jwt_required()
def delete_note(note_id):
    """删除笔记"""
    user_id = get_jwt_identity()
    note = Note.query.filter_by(id=note_id, user_id=user_id).first()
    if not note:
        return jsonify({'error': '笔记不存在'}), 404
    
    # 删除关联的图片文件
    if note.images:
        for image_path in note.images:
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], image_path)
            if os.path.exists(full_path):
                os.remove(full_path)
    
    db.session.delete(note)
    db.session.commit()
    return jsonify({'message': '笔记删除成功'}), 200

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    """上传图片"""
    if 'file' not in request.files:
        return jsonify({'error': '请选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '请选择文件'}), 400
    
    # 生成唯一文件名
    filename = str(uuid.uuid4()) + '.' + file.filename.rsplit('.', 1)[1].lower()
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # 返回相对路径
    return jsonify({'filename': filename}), 200

@bp.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    """提供图片访问"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)