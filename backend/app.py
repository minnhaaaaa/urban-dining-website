from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_cors import CORS
from models import db, User, MenuItem, Order
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv() 

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://urban_admin:urbandining%401234@localhost:5432/restaurant_db' 
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
db.init_app(app)
jwt = JWTManager(app)

# Create DB tables


# Sample data
def seed_data():
    if not MenuItem.query.first():
        db.session.add(MenuItem(name='Margherita Pizza', description='Classic cheese pizza', price=300))
        db.session.add(MenuItem(name='Burger', description='Juicy beef burger', price=99))
        db.session.commit()


@app.route('/api/google-login', methods=['POST'])
def google_login():
    data = request.get_json()
    id_token = data.get('id_token')
    if not id_token:
        return jsonify({'error': 'ID token required'}), 400
    
    try:
        resp = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={id_token}')
        if resp.status_code != 200:
            return jsonify({'error': 'Invalid token'}), 401
        user_info = resp.json()
    except Exception as e:
        return jsonify({'error': 'Token verification failed'}), 500
    
    # Find or create user
    user = User.query.filter_by(google_id=user_info['sub']).first()
    if not user:
        user = User(
            google_id=user_info['sub'],
            email=user_info['email'],
            role='admin' if user_info['email'] in ['admin@example.com'] else 'user'  # Customize admin emails
        )
        db.session.add(user)
        db.session.commit()
    
    # Generate JWT
    jwt_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'token': jwt_token})

# Fallback login (username/password)
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email'], password=data['password']).first()
    if user:
        token = create_access_token(identity={'id': user.id, 'role': user.role})
        return jsonify({'token': token})
    return jsonify({'error': 'Invalid credentials'}), 401

# Register 
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User exists'}), 400
    user = User(email=data['email'], password=data['password'], role=data.get('role', 'user'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created'})

# Get menu
@app.route('/api/menu', methods=['GET'])
def get_menu():
    items = MenuItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'image': item.image
    } for item in items])

# Add menu item (admin only)
@app.route('/api/menu', methods=['POST'])
@jwt_required()
def add_menu_item():
    claims = get_jwt_identity()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Admin required'}), 403
    data = request.get_json()
    item = MenuItem(name=data['name'], description=data['description'], price=data['price'], image=data.get('image'))
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Item added'})

# Edit menu item (admin only)
@app.route('/api/menu/<int:id>', methods=['PUT'])
@jwt_required()
def edit_menu_item(id):
    claims = get_jwt_identity()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Admin required'}), 403
    item = MenuItem.query.get_or_404(id)
    data = request.get_json()
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.image = data.get('image', item.image)
    db.session.commit()
    return jsonify({'message': 'Item updated'})

# Delete menu item (admin only)
@app.route('/api/menu/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_menu_item(id):
    claims = get_jwt_identity()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Admin required'}), 403
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'})

# Place order
@app.route('/api/orders', methods=['POST'])
@jwt_required()
def place_order():
    claims = get_jwt_identity()
    data = request.get_json()
    order = Order(user_id=claims['id'], items=json.dumps(data['items']))
    db.session.add(order)
    db.session.commit()
    return jsonify({'message': 'Order placed', 'order_id': order.id})

# Get user orders
@app.route('/api/orders', methods=['GET'])
@jwt_required()
def get_orders():
    claims = get_jwt_identity()
    orders = Order.query.filter_by(user_id=claims['id']).all()
    return jsonify([{
        'id': order.id,
        'items': json.loads(order.items),
        'status': order.status
    } for order in orders])

# Update order status (admin only)
@app.route('/api/orders/<int:id>', methods=['PUT'])
@jwt_required()
def update_order_status(id):
    claims = get_jwt_identity()
    if claims['role'] != 'admin':
        return jsonify({'error': 'Admin required'}), 403
    order = Order.query.get_or_404(id)
    data = request.get_json()
    order.status = data['status']
    db.session.commit()
    return jsonify({'message': 'Status updated'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True)