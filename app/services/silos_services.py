# app/services/silos_services.py
from logging import critical

from app.models.storage_silo import Storage
from app.db.extensions import db
from flask import abort

""" Regra de negócio para gerenciar Silos """
class StorageService:
    """Registrar Silo"""
    @staticmethod
    def create_storage(data):
        exist = Storage.query.filter_by(name=data['name']).first()

        # Valida se já existe
        if exist:
            abort(400, description=f"Silo '{data['name']}' já existe")

        # Valida capacidade
        if data['max_capacity'] <= 0:
            abort(400, description="Capacidade deve ser maior que zero")

        # Cria silo
        silo = Storage(
            name=data['name'],
            max_capacity=data['max_capacity'],
            current_occupation=data.get('current_occupation', 0),
            product=data['product'],
            local_lat=data.get('local_lat'),
            local_lng=data.get('local_lng')
        )

        db.session.add(silo)
        db.session.commit()

        return silo

    """Listar todos os silos"""
    @staticmethod
    def get_all_silos():
        return Storage.query.all()

    """Busca silo por ID"""
    @staticmethod
    def get_silo_by_id(silo_id):
        silo = Storage.query.get(silo_id)
        if not silo:
            abort(404, descripion="Silo não encontrado")
        return silo

    """Atualiza dados do silo"""
    @staticmethod
    def edit_silo(silo_id, data):
        silo = StorageService.get_silo_by_id(silo_id)

        # Atualiza campos permitidos
        if 'name' in data:
            silo.nome = data['name']
        if 'max_capacity' in data:
            if data['max_capacity'] < silo.current_occupation:
                abort(400, description="Capacidade menor que ocupação atual")
            silo.capacidade_maxima = data['max_capacity']
        if 'product' in data:
            silo.product = data['product']

        db.session.commit()
        return silo


    """ Retorna resumo geral de todos os silos """
    @staticmethod
    def dashboard():
        silos = StorageService.get_all_silos()

        if not silos:
            return {
                'summary': {
                    'total_silos': 0,
                    'total_capacity': 0,
                    'total_occupation': 0,
                    'general_percentage': 0,
                    'critical_silos': 0,
                    'ok_silos': 0
                },
                'silos': []
            }
        total_capacity = sum(s.max_capacity for s in silos)
        total_occupation = sum(s.current_occupation for s in silos)
        general_percentage = (total_occupation / total_capacity * 100) if total_capacity else 0

        critical_silos = len([s for s in silos if s.percentual_occupation >= 90])
        ok_silos = len([s for s in silos if s.percentual_occupation < 70])

        return {
            'summary': {
                'total_silos': len(silos),
                'total_capacity': total_capacity,
                'total_occupation': total_occupation,
                'general_percentage': general_percentage,
                'critical_silos': critical_silos,
                'ok_silos': ok_silos
            },
            'silos': [s.to_dict() for s in silos]
        }






