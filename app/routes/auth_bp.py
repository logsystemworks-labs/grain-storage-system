# app/routes/auth_bp.py

from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

from app.db.extensions import db
from app.models.user import User
from app.models.tenant import Tenant

auth_bp = Blueprint('auth', __name__)

""" Registra nova cooperativa + primeiro usuário """
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data['user_email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400

    if Tenant.query.filter_by(email=data['tenant_email']).first():
        return jsonify({'error': 'Cooperativa já cadastrada'}), 400

    # Cria tenant (Cooperativa)
    tenant = Tenant(
        name=data['tenant_name'],
        email=data['tenant_email'],
        phone=data.get('phone')
    )
    db.session.add(tenant)
    db.session.flush()

    # Cria usuário admin
    user = User(
        tenant_id=tenant.id,
        email=data['user_email'],
        name=data['user_name'],
        password_hash=generate_password_hash(data['password'])  # ← PASSA JÁ HASHADO
    )

    db.session.add(user)
    db.session.commit()

    # Loga automaticamente
    login_user(user)

    return jsonify({
        'message': 'Cadastro realizado com sucesso',
        'user': user.to_dict(),
        'tenant': tenant.to_dict()
    }), 201

""" Login """
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Email ou senha inválidos'}), 401

    if not user.is_active:
        return jsonify({'error': 'Usuário inativo'}), 403

    login_user(user)

    return jsonify({
        'message': 'Login realizado com sucesso',
        'user': user.to_dict()
    })


"""Logout"""
@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout realizado com sucesso'})


"""Retorna usuário logado"""
@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        'user': current_user.to_dict(),
        'tenant': current_user.tenant.to_dict()
    })