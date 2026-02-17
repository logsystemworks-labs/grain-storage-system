# app/routes/silos_bp.py

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app.services.silos_services import StorageService

silos_bp = Blueprint('silos', __name__)


""" Cria novo silo """
@silos_bp.route('/', methods=['POST'])
@login_required
def create_silo():
    data = request.get_json()
    tenant_id = current_user.tenant_id
    silo = StorageService.create_storage(data, tenant_id)
    return jsonify(silo.to_dict()), 201


""" Lista todos os silos """
@silos_bp.route('/', methods=['GET'])
@login_required
def get_list_silos():
    tenant_id = current_user.tenant_id
    silos = StorageService.get_all_silos(tenant_id)
    return jsonify([s.to_dict() for s in silos])


""" Lista um silo """
@silos_bp.route('/<int:silo_id>', methods=['GET'])
@login_required
def get_by_id(silo_id):
    tenant_id = current_user.tenant_id
    silo = StorageService.get_silo_by_id(silo_id, tenant_id)
    return jsonify(silo.to_dict())


""" Update silo """
@silos_bp.route('/<int:silo_id>', methods=['PUT'])
@login_required
def update_silo(silo_id):
    data = request.get_json()
    tenant_id = current_user.tenant_id
    silo = StorageService.edit_silo(silo_id, data, tenant_id)
    return jsonify(silo.to_dict())


""" Dashboard geral """
@silos_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    tenant_id = current_user.tenant_id
    datas = StorageService.dashboard(tenant_id)
    return jsonify(datas)

