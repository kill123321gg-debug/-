from flask import Flask
from flask_cors import CORS
import os

app = Flask(__name__)

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///campus_book.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# 启用CORS
CORS(app)

# 导入扩展
from extensions import db

# 初始化数据库
db.init_app(app)

# 导入模型
from models.models import User, Book, Order, Address

# 导入路由蓝图
from routes.user import user_bp
from routes.book import book_bp
from routes.order import order_bp
from routes.address import address_bp

# 注册蓝图
app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(order_bp)
app.register_blueprint(address_bp)

if __name__ == '__main__':
    # 创建数据库表
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)