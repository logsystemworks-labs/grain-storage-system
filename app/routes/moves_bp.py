from flask import Blueprint, request, jsonify
from app.services.movements_services import MovementsService

moves_bp = Blueprint('movements', __name__)

""" Registra entrada ou saída de grãos """
@moves_bp.route('/', methods=['POST'])
def create_mov():
    data = request.get_json()
    movement = MovementsService.create_movements(data)
    return jsonify(movement.to_dict()), 201

""" Lista movimentações """
@moves_bp.route('/', methods=['GET'])
def get_all_movements():
    silo_id = request.args.get('silo_id', type=int)
    types = request.args.get('types')
    limit = request.args.get('limit', 50, type=int)

    movements = MovementsService.get_all_moves(silo_id, types, limit)
    return jsonify([m.to_dict() for m in movements])


"""Estatísticas de um silo"""
@moves_bp.route('/statistics/<int:silo_id>', methods=['GET'])
def silo_stats(silo_id):
    stats = MovementsService.silo_statistics(silo_id)
    return jsonify(stats)

