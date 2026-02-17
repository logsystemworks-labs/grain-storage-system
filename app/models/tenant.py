# app/models/tenant.py
from app.db.extensions import db
from datetime import datetime


class Tenant(db.Model):
    __tablename__ = 'tenants'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # "Cooperativa ABC"
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    is_active = db.Column(db.Boolean, default=True)

    # Relacionamentos
    silos = db.relationship('Storage', backref='tenant', lazy=True)
    users = db.relationship('User', backref='tenant', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

    def __repr__(self):
        return f'<Tenant {self.name}>'