# app/routes/auth_bp.py

from flask import Blueprint, request, jsonify, redirect, url_for, render_template, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import secrets
from datetime import datetime, timedelta
from app.db.extensions import db
from app.models.user import User
from app.models.tenant import Tenant
from config import logger

auth_bp = Blueprint('auth', __name__)

""" Registra nova cooperativa + primeiro usuário """
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if User.query.filter_by(email=data['user_email']).first():
        return jsonify({'error': 'Email já cadastrado'}), 400

    if Tenant.query.filter_by(email=data['tenant_email']).first():
        return jsonify({'error': 'Cooperativa já cadastrada'}), 400

    tenant = Tenant(
        name=data['tenant_name'],
        email=data['tenant_email'],
        phone=data.get('phone')
    )
    db.session.add(tenant)
    db.session.flush()

    user = User(
        tenant_id=tenant.id,
        email=data['user_email'],
        name=data['user_name'],
        password_hash=generate_password_hash(data['password'])
    )

    db.session.add(user)
    db.session.commit()
    login_user(user)

    return jsonify({
        'message': 'Cadastro realizado com sucesso',
        'user': user.to_dict(),
        'tenant': tenant.to_dict()
    }), 201

""" Login """
@auth_bp.route('/login', methods=['GET','POST'])
def login():

    if request.method == 'GET':
        return render_template('auth/login.html')

    if request.is_json:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        remember = data.get('remember', False)

        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return jsonify({'error': 'Email ou senha inválidos'}), 401

        if not user.is_active:
            return jsonify({'error': 'Usuário inativo'}), 403

        login_user(user, remember=remember)
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': user.to_dict()
        })
    # ── POST via formulário HTML ───────────────────────────────
    email = request.form.get('email')
    password = request.form.get('password')
    remember = request.form.get('remember') == 'on'

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        flash('Email ou senha inválidos', 'error')
        return redirect(url_for('auth.login'))

    if not user.is_active:
        flash('Usuário inativo', 'error')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    return redirect(url_for('dashboard.index'))  # ← ajusta pro nome da sua rota de dashboard


"""Logout"""
@auth_bp.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    if request.accept_mimetypes.accept_html:
        return redirect(url_for('auth.login'))

    return jsonify({'message': 'Logout realizado com sucesso'})


"""Retorna usuário logado"""
@auth_bp.route('/me', methods=['GET'])
@login_required
def me():
    return jsonify({
        'user': current_user.to_dict(),
        'tenant': current_user.tenant.to_dict()
    })


"""Retorna usuário logado"""
@auth_bp.route('/forget', methods=['GET','POST'])
def forget():

    if request.method == 'GET':
        return render_template('auth/forget.html')

    # POST - processa o email
    email = request.form.get('email')
    user = User.query.filter_by(email=email).first()

    # SEMPRE mostra a mesma mensagem
    msg = 'Se esse email estiver cadastrado, você receberá as instruções.'

    if user:
        # Gera token único
        token = secrets.token_urlsafe(32)

        # Salva no usuário (precisa campos no model)
        user.reset_token = token
        user.reset_token_expiry = datetime.now() + timedelta(hours=1)
        db.session.commit()

        # Link de reset
        link = url_for('auth.reset_pass', token=token, _external=True)

        # Por agora - printa no terminal (depois integra email)
        logger.info(f"\n🔑 LINK DE RESET: {link}\n")
    flash(msg, 'success')
    return redirect(url_for('auth.forget'))


@auth_bp.route('/reset-pass/<token>', methods=['GET', 'POST'])
def reset_pass(token):

    # Busca usuário pelo token
    user = User.query.filter_by(reset_token=token).first()

    # Token inválido ou expirado
    if not user or user.reset_token_expiry < datetime.now():
        flash('LINK inválido ou expirado.', 'error')
        return redirect(url_for('auth.forget'))

    if request.method == 'GET':
        return render_template('auth/reset_pass.html', token=token)

    # POST - salva nova senha
    new_pass = request.form.get('password')

    user.set_password(new_pass)
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()

    flash('Senha redefinida com sucesso', 'success')
    return redirect(url_for('auth.login'))



