from app.db.extensions import db

""" Modelo para tabela no DB via Python """
class Storage(db.Model):
    __tablename__='silos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)            # "Silo A - Milho"
    max_capacity = db.Column(db.Float, nullable=False)          # 250 (Toneladas)
    current_occupation = db.Column(db.Float, nullable=False)    # 230 (Toneladas)
    product = db.Column(db.String(255), nullable=False)         # "Milho", "Soja", etc
    local_lat = db.Column(db.Float, nullable=False)
    local_lng = db.Column(db.Float, nullable=False)

    # Relacionamento
    movements = db.relationship("Movements", back_populates="silo", cascade="all, delete-orphan")

    """ Calcula o percentual de capacidade atual do Silo """
    @property
    def percentual_occupation(self):
        return (self.current_occupation / self.max_capacity) * 100

    """ Calcula espaço disponível """
    @property
    def available_capacity(self) -> float:
        return self.max_capacity - self.current_occupation

    """ Status do silo """
    @property
    def status(self) -> str:
        if self.percentual_occupation >= 90:
            return "CRÍTICO"
        elif self.percentual_occupation >= 70:
            return "ATENÇÃO"
        else:
            return "OK"

    """Serializa pra JSON"""
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'max_capacity': self.max_capacity,
            'current_occupation': self.current_occupation,
            'percentual_occupation': round(self.percentual_occupation, 2),
            'available_capacity': self.available_capacity,
            'product': self.product,
            'status': self.status,
            'localization': {
                'lat': self.local_lat,
                'lng': self.local_lng
            } if self.local_lat else None
        }
