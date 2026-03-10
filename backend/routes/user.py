from flask import Blueprint, request, jsonify
from models.models import User
from extensions import db
from passlib.hash import sha256_crypt
import re

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/user/register', methods=['POST'])
def register():
    """用户注册"""
    data = request.get_json()
    
    # 验证数据
    if not data.get('username') or not data.get('password') or not data.get('nickname'):
        return jsonify({'code': 400, 'message': '缺少必填字段'}), 400
    
    # 验证邮箱或手机号
    if data.get('email') and not re.match(r'^[a-zA-Z0-9._%+-]+@gzus\.edu\.cn$', data.get('email')):
        return jsonify({'code': 400, 'message': '邮箱必须是@gzus.edu.cn域名'}), 400
    
    if data.get('phone') and not re.match(r'^1[3-9]\d{9}$', data.get('phone')):
        return jsonify({'code': 400, 'message': '手机号格式不正确'}), 400
    
    # 验证密码长度
    if len(data.get('password')) < 6 or len(data.get('password')) > 20:
        return jsonify({'code': 400, 'message': '密码长度必须在6-20位之间'}), 400
    
    # 检查用户名是否已存在
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'code': 400, 'message': '用户名已存在'}), 400
    
    # 检查邮箱是否已存在
    if data.get('email') and User.query.filter_by(email=data.get('email')).first():
        return jsonify({'code': 400, 'message': '邮箱已被注册'}), 400
    
    # 检查手机号是否已存在
    if data.get('phone') and User.query.filter_by(phone=data.get('phone')).first():
        return jsonify({'code': 400, 'message': '手机号已被注册'}), 400
    
    # 创建新用户
    hashed_password = sha256_crypt.hash(data.get('password'))
    new_user = User(
        username=data.get('username'),
        password=hashed_password,
        nickname=data.get('nickname'),
        avatar=data.get('avatar'),
        phone=data.get('phone'),
        email=data.get('email')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '注册成功', 'user_id': new_user.id}), 200

@user_bp.route('/api/user/login', methods=['POST'])
def login():
    """用户登录"""
    data = request.get_json()
    
    # 验证数据
    if not data.get('username') or not data.get('password'):
        return jsonify({'code': 400, 'message': '缺少用户名或密码'}), 400
    
    # 查找用户
    user = User.query.filter_by(username=data.get('username')).first()
    
    if not user or not sha256_crypt.verify(data.get('password'), user.password):
        return jsonify({'code': 401, 'message': '用户名或密码错误'}), 401
    
    return jsonify({'code': 200, 'message': '登录成功', 'user': {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'phone': user.phone,
        'email': user.email
    }}), 200

@user_bp.route('/api/user/profile', methods=['GET'])
def get_profile():
    """获取用户信息"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'}), 400
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    
    return jsonify({'code': 200, 'user': {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'phone': user.phone,
        'email': user.email
    }}), 200

@user_bp.route('/api/user/profile', methods=['PUT'])
def update_profile():
    """更新用户信息"""
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'}), 400
    
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404
    
    # 更新用户信息
    if data.get('nickname'):
        user.nickname = data.get('nickname')
    
    if data.get('avatar'):
        user.avatar = data.get('avatar')
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '更新成功', 'user': {
        'id': user.id,
        'username': user.username,
        'nickname': user.nickname,
        'avatar': user.avatar,
        'phone': user.phone,
        'email': user.email
    }}), 200