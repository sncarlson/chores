"""
TODO Specifies endpoints and behavior for at least:
    Two GET requests
    One POST request
    One PATCH request
    One DELETE request
    Utilize the @app.errorhandler decorator to format error responses as JSON objects
    for at least four different status codes
"""

from flask import Blueprint, jsonify
from model.models import Area

# Blueprint Configuration
controller_bp = Blueprint(
    'controller_bp', __name__,
)


@controller_bp.route('/chores', methods=['GET'])
def chores():
    return "Hello from the controller!"


@controller_bp.route('/chores', methods=['POST'])
def create_chores():
    return "Hello from the controller!"


@controller_bp.route('/chores/<chore_id>', methods=['DELETE'])
def delete_chore(chore_id):
    return "Hello from the controller!"


@controller_bp.route('/chores/<chore_id>', methods=['PATCH'])
def update_chore(chore_id):
    return "Hello from the controller!"


@controller_bp.route('/areas', methods=['GET'])
def areas():
    all_areas = Area.query.all()

    data = [area.format() for area in all_areas]

    result = {
        "success": True,
        "areas": data
    }
    return jsonify(result)


@controller_bp.route('/areas', methods=['POST'])
def create_area():
    return "Hello from the controller!"


@controller_bp.route('/areas/<area_id>', methods=['DELETE'])
def delete_area(area_id):
    return "Hello from the controller!"


@controller_bp.route('/areas/<area_id>', methods=['PATCH'])
def update_area(area_id):
    return "Hello from the controller!"


@controller_bp.route('/workers', methods=['GET'])
def workers():
    return "Hello from the controller!"


@controller_bp.route('/workers', methods=['POST'])
def create_worker():
    return "Hello from the controller!"


@controller_bp.route('/workers/<worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    return "Hello from the controller!"


@controller_bp.route('/workers/<worker_id>', methods=['PATCH'])
def update_worker(worker_id):
    return "Hello from the controller!"


@controller_bp.route('/assigned-chores', methods=['GET'])
def assigned_chores():
    return "Hello from the controller!"


@controller_bp.route('/assigned-chores', methods=['POST'])
def assign_chore():
    return "Hello from the controller!"


@controller_bp.route('/assigned-chores/<assigned_chore_id>', methods=['DELETE'])
def delete_assigned_chore(assigned_chore_id):
    return "Hello from the controller!"


@controller_bp.route('/assigned-chores/<assigned_chore_id>', methods=['PATCH'])
def update_assigned_chore(assigned_chore_id):
    return "Hello from the controller!"
