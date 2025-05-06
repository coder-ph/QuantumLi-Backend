from flask import Blueprint, request, jsonify
from src.handlers.controllers.employee_controller import (
    create_employee,
    get_employee,
    get_all_employees,
    update_employee,
    delete_employee
)

employee_bp = Blueprint('employee_bp', __name__)

@employee_bp.route('/employees', methods=['POST'])
def create_employee_route():
    return create_employee()

@employee_bp.route('/employees', methods=['GET'])
def get_all_employees_route():
    return get_all_employees()

@employee_bp.route('/employees/<uuid:employee_id>', methods=['GET'])
def get_employee_route(employee_id):
    return get_employee(employee_id)

@employee_bp.route('/employees/<uuid:employee_id>', methods=['PUT'])
def update_employee_route(employee_id):
    return update_employee(employee_id)

@employee_bp.route('/employees/<uuid:employee_id>', methods=['DELETE'])
def delete_employee_route(employee_id):
    return delete_employee(employee_id)
