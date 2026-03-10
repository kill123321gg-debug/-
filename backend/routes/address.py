from flask import Blueprint, request, jsonify
from models.models import Address
from extensions import db

address_bp = Blueprint('address', __name__)

@address_bp.route('/api/addresses', methods=['GET'])
def get_addresses():
    """获取地址列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'}), 400
    
    addresses = Address.query.filter_by(user_id=user_id).all()
    
    address_list = []
    for address in addresses:
        address_list.append({
            'id': address.id,
            'receiver': address.receiver,
            'phone': address.phone,
            'address': address.address,
            'is_default': address.is_default
        })
    
    return jsonify({'code': 200, 'addresses': address_list}), 200

@address_bp.route('/api/addresses', methods=['POST'])
def create_address():
    """新增地址"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['user_id', 'receiver', 'phone', 'address']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400
    
    # 如果设置为默认地址，先将其他地址设为非默认
    if data.get('is_default'):
        Address.query.filter_by(user_id=data.get('user_id')).update({'is_default': False})
    
    # 创建地址
    new_address = Address(
        user_id=data.get('user_id'),
        receiver=data.get('receiver'),
        phone=data.get('phone'),
        address=data.get('address'),
        is_default=data.get('is_default', False)
    )
    
    db.session.add(new_address)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '地址添加成功', 'address_id': new_address.id}), 200

@address_bp.route('/api/addresses/<int:address_id>', methods=['PUT'])
def update_address(address_id):
    """更新地址"""
    data = request.get_json()
    address = Address.query.get(address_id)
    
    if not address:
        return jsonify({'code': 404, 'message': '地址不存在'}), 404
    
    # 如果设置为默认地址，先将其他地址设为非默认
    if data.get('is_default'):
        Address.query.filter_by(user_id=address.user_id).update({'is_default': False})
    
    # 更新地址信息
    if data.get('receiver'):
        address.receiver = data.get('receiver')
    if data.get('phone'):
        address.phone = data.get('phone')
    if data.get('address'):
        address.address = data.get('address')
    if 'is_default' in data:
        address.is_default = data.get('is_default')
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '地址更新成功'}), 200

@address_bp.route('/api/addresses/<int:address_id>', methods=['DELETE'])
def delete_address(address_id):
    """删除地址"""
    address = Address.query.get(address_id)
    
    if not address:
        return jsonify({'code': 404, 'message': '地址不存在'}), 404
    
    db.session.delete(address)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '地址删除成功'}), 200