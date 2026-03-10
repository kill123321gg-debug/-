from flask import Blueprint, request, jsonify
from models.models import Book
from extensions import db
import os

book_bp = Blueprint('book', __name__)

@book_bp.route('/api/books', methods=['GET'])
def get_books():
    """获取书籍列表"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    category = request.args.get('category')
    
    query = Book.query.filter_by(status='available')
    
    if category:
        query = query.filter_by(category=category)
    
    pagination = query.order_by(Book.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    books = pagination.items
    
    book_list = []
    for book in books:
        book_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'category': book.category,
            'condition': book.condition,
            'price': book.price,
            'stock': book.stock,
            'delivery_type': book.delivery_type,
            'images': book.images.split(',') if book.images else [],
            'user_id': book.user_id,
            'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'code': 200, 'books': book_list, 'total': pagination.total, 'pages': pagination.pages}), 200

@book_bp.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """获取书籍详情"""
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'}), 404
    
    return jsonify({'code': 200, 'book': {
        'id': book.id,
        'title': book.title,
        'author': book.author,
        'isbn': book.isbn,
        'category': book.category,
        'condition': book.condition,
        'price': book.price,
        'description': book.description,
        'stock': book.stock,
        'delivery_type': book.delivery_type,
        'images': book.images.split(',') if book.images else [],
        'user_id': book.user_id,
        'status': book.status,
        'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S')
    }}), 200

@book_bp.route('/api/books', methods=['POST'])
def create_book():
    """发布书籍"""
    data = request.get_json()
    
    # 验证数据
    required_fields = ['title', 'category', 'condition', 'price', 'delivery_type', 'user_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400
    
    # 创建书籍
    new_book = Book(
        title=data.get('title'),
        author=data.get('author'),
        isbn=data.get('isbn'),
        category=data.get('category'),
        condition=data.get('condition'),
        price=data.get('price'),
        description=data.get('description'),
        stock=data.get('stock', 1),
        delivery_type=data.get('delivery_type'),
        images=','.join(data.get('images', [])),
        user_id=data.get('user_id')
    )
    
    db.session.add(new_book)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '发布成功', 'book_id': new_book.id}), 200

@book_bp.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """更新书籍"""
    data = request.get_json()
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'}), 404
    
    # 更新书籍信息
    if data.get('title'):
        book.title = data.get('title')
    if data.get('author'):
        book.author = data.get('author')
    if data.get('isbn'):
        book.isbn = data.get('isbn')
    if data.get('category'):
        book.category = data.get('category')
    if data.get('condition'):
        book.condition = data.get('condition')
    if data.get('price'):
        book.price = data.get('price')
    if data.get('description'):
        book.description = data.get('description')
    if data.get('stock'):
        book.stock = data.get('stock')
    if data.get('delivery_type'):
        book.delivery_type = data.get('delivery_type')
    if data.get('images'):
        book.images = ','.join(data.get('images'))
    
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '更新成功'}), 200

@book_bp.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """删除书籍"""
    book = Book.query.get(book_id)
    
    if not book:
        return jsonify({'code': 404, 'message': '书籍不存在'}), 404
    
    db.session.delete(book)
    db.session.commit()
    
    return jsonify({'code': 200, 'message': '删除成功'}), 200

@book_bp.route('/api/books/search', methods=['GET'])
def search_books():
    """搜索书籍"""
    keyword = request.args.get('keyword')
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    condition = request.args.get('condition')
    
    query = Book.query.filter_by(status='available')
    
    if keyword:
        query = query.filter(Book.title.like(f'%{keyword}%'))
    if category:
        query = query.filter_by(category=category)
    if min_price is not None:
        query = query.filter(Book.price >= min_price)
    if max_price is not None:
        query = query.filter(Book.price <= max_price)
    if condition:
        query = query.filter_by(condition=condition)
    
    books = query.order_by(Book.created_at.desc()).all()
    
    book_list = []
    for book in books:
        book_list.append({
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'isbn': book.isbn,
            'category': book.category,
            'condition': book.condition,
            'price': book.price,
            'stock': book.stock,
            'delivery_type': book.delivery_type,
            'images': book.images.split(',') if book.images else [],
            'user_id': book.user_id,
            'created_at': book.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return jsonify({'code': 200, 'books': book_list, 'total': len(book_list)}), 200