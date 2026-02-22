# app/models/user.py

from app.db.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

""" Usuário do sistema (pode ter vários tenant) """
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)


    """Hash da senha"""
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    """Verifica senha"""
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'tenant_id': self.tenant_id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<User {self.email}>'