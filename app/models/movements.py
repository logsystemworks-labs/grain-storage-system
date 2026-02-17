from app.db.extensions import db
from datetime import datetime

""" Modelo para tabela no DB via Python """
class Movements(db.Model):
    __tablename__='movements'

    id = db.Column(db.Integer, primary_key=True)
    tenant_id = db.Column(db.Integer, db.ForeignKey('tenants.id'), nullable=False)
    silo_id = db.Column(db.Integer,db.ForeignKey("silos.id"), nullable=False)       # FK
    types = db.Column(db.String(10), nullable=False)                                 # ENTRADA / SAIDA
    amount = db.Column(db.Float, nullable=False)                                    # Quantidade 30 (Toneladas)
    product = db.Column(db.String(255), nullable=False)                             # "Milho"

    origin = db.Column(db.String(255))                                              # "Fazenda Santa Rita" (se entrada)
    destination = db.Column(db.String(255))                                         # "Moinho X" (se saída)

    truck_plate = db.Column(db.String(20))                                          # ABC-1234
    driver = db.Column(db.String(255))                                              # "João Silva"
    responsible = db.Column(db.String(255))                                         # "Maria (operadora)"

    observations = db.Column(db.Text)

    timestamp = db.Column(db.DateTime, default=datetime.now,nullable=False)

    # RELACIONAMENTO
    silo = db.relationship("Storage", back_populates="movements")

    """Serializa pra JSON"""
    def to_dict(self):
        return {
            'id': self.id,
            'silo_id': self.silo_id,
            'silo_name': self.silo.name if self.silo else None,
            'types': self.types,
            'amount': self.amount,
            'product': self.product,
            'origin': self.origin,
            'destination': self.destination,
            'truck_plate': self.truck_plate,
            'driver': self.driver,
            'responsible': self.responsible,
            'observations': self.observations,
            'timestamp': self.timestamp.isoformat()
        }

    def __repr__(self):
        return f'<Movements {self.id} - {self.types} {self.amount}t>'
