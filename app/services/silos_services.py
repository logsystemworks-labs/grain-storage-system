# app/services/silos_services.py
from app.models.storage_silo import Storage
from app.db.extensions import db
from flask import abort

""" Regra de negócio para gerenciar Silos """
class StorageService:
    """Registrar Silo"""
    @staticmethod
    def create_storage(data, tenant_id):
        exist = Storage.query.filter_by(tenant_id=tenant_id, name=data['name']).first()

        # Valida se já existe
        if exist:
            abort(400, description=f"Silo '{data['name']}' já existe")

        # Valida capacidade
        if data['max_capacity'] <= 0:
            abort(400, description="Capacidade deve ser maior que zero")

        # Cria silo
        silo = Storage(
            tenant_id=tenant_id,  # ← Adiciona tenant_id
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

    """Listar todos os silos de um tenant específico"""
    @staticmethod
    def get_all_silos(tenant_id):
        return Storage.query.filter_by(tenant_id=tenant_id).all()

    """Busca silo por ID (dentro do tenant)"""
    @staticmethod
    def get_silo_by_id(silo_id, tenant_id):
        silo = Storage.query.filter_by(id=silo_id, tenant_id=tenant_id).first()
        if not silo:
            abort(404, descripion="Silo não encontrado")
        return silo

    """Atualiza dados do silo"""
    @staticmethod
    def edit_silo(silo_id, data, tenant_id):
        silo = StorageService.get_silo_by_id(silo_id, tenant_id)

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
    def dashboard(tenant_id):
        silos = StorageService.get_all_silos(tenant_id)

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
                'total_capacity': round(total_capacity, 2),
                'total_occupation': round(total_occupation, 2),
                'general_percentage': round(general_percentage, 2),
                'critical_silos': critical_silos,
                'ok_silos': ok_silos
            },
            'silos': [s.to_dict() for s in silos]
        }






