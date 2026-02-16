# app/routes/silos_bp.py

from flask import Blueprint, request, jsonify
from app.services.silos_services import StorageService

silos_bp = Blueprint('silos', __name__)


""" Cria novo silo """
@silos_bp.route('/', methods=['POST'])
def create_silo():
    data = request.get_json()
    silo = StorageService.create_storage(data)
    return jsonify(silo.to_dict()), 201


""" Lista todos os silos """
@silos_bp.route('/', methods=['GET'])
def get_list_silos():
    silos = StorageService.get_all_silos()
    return jsonify([s.to_dict() for s in silos])


""" Lista um silo """
@silos_bp.route('/<int:silo_id>', methods=['GET'])
def get_by_id(silo_id):
    silo = StorageService.get_silo_by_id(silo_id)
    return jsonify(silo.to_dict())


""" Update silo """
@silos_bp.route('/<int:silo_id>', methods=['PUT'])
def update_silo(silo_id):
    data = request.get_json()
    silo = StorageService.edit_silo(silo_id, data)
    return jsonify(silo.to_dict())


""" Dashboard geral """
@silos_bp.route('/dashboard', methods=['GET'])
def dashboard():
    datas = StorageService.dashboard()
    return jsonify(datas)

