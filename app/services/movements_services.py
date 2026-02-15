# app/services/movements_services.py

from app.db.extensions import db
from app.models.storage_silo import Storage
from app.models.movements import Movements
from flask import abort

""" Serviço com TODA lógica de negócio de movimentações """
class MovementsService:

    @staticmethod
    def create_movements(data):

        # 1. Validações básicas
        MovementsService._validate_input_data(data)

        # 2. Busca silo
        silo = Storage.query.get(data['silo_id'])
        if not silo:
            abort(404, description="Silo não encontrado")

        # 3. Valida produto
        if silo.product != data['product']:
            abort(400, description=f"Silo armazena {silo.product}, não {data['product']}")

        # 4. Calcula nova ocupação
        types = data['types'].upper()
        amount = data['amount']

        if types == "ENTRADA":
            new_occupation = silo.current_occupation + amount
        elif types == "SAIDA":
            new_occupation = silo.current_occupation - amount
        else:
            abort(400, description="Tipo deve ser ENTRADA ou SAIDA")

        # 5. Valida limites
        MovementsService.validate_limits(silo, new_occupation, amount)

        # 6. Cria movimentação
        movement = Movements(
            silo_id=data['silo_id'],
            types=types,
            amount=amount,
            product=data['product'],
            origin=data.get('origin'),
            destination=data.get('destination'),
            truck_plate=data.get('truck_plate'),
            driver=data.get('driver'),
            responsible=data['responsible'],
            observations=data.get('observations')
        )

        # 7. Atualiza silo
        silo.current_occupation = new_occupation

        # 8. Salva
        db.session.add(movement)
        db.session.commit()

        # 9. Verifica alertas
        MovementsService._check_alerts(silo)

        return movement

    """Valida dados de entrada"""
    @staticmethod
    def _validate_input_data(data):
        # Campos obrigatórios
        required_fields = ['silo_id', 'type', 'amount', 'product', 'responsible']
        for field in required_fields:
            if field not in data or not data[field]:
                abort(400, description=f"Campo '{field}' é obrigatório")

        # Quantidade positiva
        if data['amount'] <= 0:
            abort(400, description="Quantidade deve ser maior que zero")

        # Tipo válido
        types = data['types'].upper()
        if types not in ['ENTRADA', 'SAIDA']:
            abort(400, description="Tipo deve ser ENTRADA ou SAIDA")

        # Origem obrigatória se ENTRADA
        if types == 'ENTRADA' and not data.get('origin'):
            abort(400, description="Origem obrigatória para ENTRADA")

        # Destino obrigatório se SAIDA
        if types == 'SAIDA' and not data.get('destination'):
            abort(400, description="Destino obrigatório para SAIDA")

    """Valida se operação respeita limites"""
    @staticmethod
    def validate_limits(silo, new_occupation, amount):
        # Não pode exceder capacidade
        if new_occupation > silo.max_capacity:
            available = silo.available_capacity
            abort(400, description=(
                f"Capacidade insuficiente. "
                f"Tentando adicionar {amount}t, "
                f"mas só há {available}t disponíveis no silo '{silo.name}'"
            ))

        # Não pode ficar negativo
        if new_occupation < 0:
            abort(400, description=(
                f"Estoque insuficiente. "
                f"Silo '{silo.name}' tem {silo.current_occupation}t, "
                f"não é possível retirar {amount}t"
            ))

    """Verifica e loga alertas"""
    @staticmethod
    def _check_alerts(silo):
        percentage = silo.percentual_occupation
        if percentage >= 95:
            print(f"🚨 ALERTA CRÍTICO: Silo '{silo.nome}' em {percentage:.1f}%")
            # TODO: Enviar notificação

        elif percentage >= 90:
            print(f"⚠️  ALERTA: Silo '{silo.nome}' em {percentage:.1f}%")

        elif 10 >= percentage > 0:
            print(f"📉 INFO: Silo '{silo.nome}' quase vazio ({percentage:.1f}%)")


    """ Retorna estatisticas de um silo """
    @staticmethod
    def silo_statistics(silo_id):
        silo = Storage.query.get(silo_id)
        if not silo:
            abort(404, description="Silo não encontrado")

        movements = Movements.query.filter_by(silo_id=silo_id).all()

        total_inputs = sum(m.amount for m in movements if m.types == "ENTRADA")
        total_outputs = sum(m.amount for m in movements if m.types == "SAIDA")

        return {
            "silo": silo.to_dict(),
            "statistics": {
                "total_movements": len(movements),
                "total_inputs": total_inputs,
                "total_outputs": total_outputs,
                "current_occupation": silo.current_occupation,
                "percentage": silo.occupancy_percentage,
                "status": silo.status
            }
        }