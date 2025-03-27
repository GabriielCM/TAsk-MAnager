from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registrar um novo usuário
    """
    data = request.get_json()
    
    # Verificar se o e-mail já está em uso
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({'message': 'Email já está em uso', 'status': 'error'}), 400
    
    # Verificar se o nome de usuário já está em uso
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({'message': 'Nome de usuário já está em uso', 'status': 'error'}), 400
    
    # Criar o novo usuário
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        password=data.get('password')
    )
    
    db.session.add(user)
    db.session.commit()
    
    # Gerar token de acesso
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Usuário registrado com sucesso',
        'status': 'success',
        'access_token': access_token,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Autenticar um usuário existente
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    # Buscar o usuário pelo e-mail
    user = User.query.filter_by(email=email).first()
    
    # Verificar a senha
    if user and user.check_password(password):
        # Gerar token de acesso
        access_token = create_access_token(identity=user.id)
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'status': 'success',
            'access_token': access_token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200
    
    return jsonify({'message': 'Credenciais inválidas', 'status': 'error'}), 401

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    """
    Obter o perfil do usuário autenticado
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'status': 'error'}), 404
    
    return jsonify({
        'status': 'success',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.isoformat()
        }
    }), 200

@auth_bp.route('/update-profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """
    Atualizar o perfil do usuário autenticado
    """
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'message': 'Usuário não encontrado', 'status': 'error'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    if 'username' in data and data['username'] != user.username:
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'message': 'Nome de usuário já está em uso', 'status': 'error'}), 400
        user.username = data['username']
    
    if 'email' in data and data['email'] != user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'message': 'Email já está em uso', 'status': 'error'}), 400
        user.email = data['email']
    
    if 'password' in data:
        user.set_password(data['password'])
    
    db.session.commit()
    
    return jsonify({
        'message': 'Perfil atualizado com sucesso',
        'status': 'success',
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }
    }), 200