from flask import Blueprint, request, jsonify
from models.models import Order, Book, Address
from extensions import db
import uuid
from datetime import datetime

order_bp = Blueprint('order', __name__)

@order_bp.route('/api/orders', methods=['POST'])
def create_order():
    """创建订单"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['user_id', 'book_id', 'address_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400
    
    # 检查书籍是否存在且有库存
    book = Book.query.get(data.get('book_id'))
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'}), 404
    
    if book.stock <= 0:
        return jsonify({'code': 400, 'message': '书籍库存不足'}), 400
    
    # 检查地址是否存在
    address = Address.query.get(data.get('address_id'))
    if not address:
        return jsonify({'code': 404, 'message': '地址不存在'}), 404
    
    # 生成订单号
    order_no = str(uuid.uuid4()).replace('-', '')[:16]
    
    # 创建订单
    new_order = Order(
        order_no=order_no,
        user_id=data.get('user_id'),
        book_id=data.get('book_id'),
        address_id=data.get('address_id'),
        total_price=book.price,
        status='pending'
    )
    
    # 减少书籍库存
    book.stock -= 1
    if book.stock == 0:
        book.status = 'sold'
    
    db.session.add(new_order)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '订单创建成功', 'order_id': new_order.id, 'order_no': order_no}), 200

@order_bp.route('/api/orders', methods=['GET'])
def get_orders():
    """获取订单列表"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'code': 400, 'message': '缺少用户ID'}), 400
    
    orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    
    order_list = []
    for order in orders:
        # 获取书籍信息
        book = Book.query.get(order.book_id)
        # 获取地址信息
        address = Address.query.get(order.address_id)
        
        order_list.append({
            'id': order.id,
            'order_no': order.order_no,
            'book': {
                'id': book.id,
                'title': book.title,
                'price': book.price,
                'images': book.images.split(',') if book.images else []
            },
            'address': {
                'receiver': address.receiver,
                'phone': address.phone,
                'address': address.address
            },
            'total_price': order.total_price,
            'status': order.status,
            'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'code': 200, 'orders': order_list}), 200

@order_bp.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """获取订单详情"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在'}), 404
    
    # 获取书籍信息
    book = Book.query.get(order.book_id)
    # 获取地址信息
    address = Address.query.get(order.address_id)
    
    return jsonify({'code': 200, 'order': {
        'id': order.id,
        'order_no': order.order_no,
        'book': {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': book.price,
            'images': book.images.split(',') if book.images else []
        },
        'address': {
            'receiver': address.receiver,
            'phone': address.phone,
            'address': address.address
        },
        'total_price': order.total_price,
        'status': order.status,
        'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
        'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S')
    }}), 200

@order_bp.route('/api/orders/<int:order_id>/cancel', methods=['PUT'])
def cancel_order(order_id):
    """取消订单"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在'}), 404
    
    if order.status != 'pending':
        return jsonify({'code': 400, 'message': '只有待付款订单可以取消'}), 400
    
    # 恢复书籍库存
    book = Book.query.get(order.book_id)
    book.stock += 1
    book.status = 'available'
    
    # 更新订单状态
    order.status = 'cancelled'
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '订单取消成功'}), 200

@order_bp.route('/api/orders/<int:order_id>/confirm', methods=['PUT'])
def confirm_order(order_id):
    """确认收货"""
    order = Order.query.get(order_id)
    
    if not order:
        return jsonify({'code': 404, 'message': '订单不存在'}), 404
    
    if order.status != 'shipped':
        return jsonify({'code': 400, 'message': '只有待收货订单可以确认收货'}), 400
    
    # 更新订单状态
    order.status = 'completed'
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '收货确认成功'}), 200