"""
TODO Specifies endpoints and behavior for at least:
    Two GET requests
    One POST request
    One PATCH request
    One DELETE request
    Utilize the @app.errorhandler decorator to format error responses as JSON objects
    for at least four different status codes
"""
import sys

import werkzeug
from flask import Blueprint, jsonify, abort, request
from model.models import Area, Chore, Worker, AssignedChores, db

# Blueprint Configuration
controller_bp = Blueprint(
    'controller_bp', __name__,
)


@controller_bp.route('/chores', methods=['GET'])
def chores():
    all_chores = Chore.query.all()

    if len(all_chores) == 0:
        abort(404)

    data = [chore.format() for chore in all_chores]

    result = {
        "success": True,
        "areas": data
    }
    return jsonify(result)


@controller_bp.route('/chores', methods=['POST'])
def create_chores():
    description = request.json.get('description')
    cost = request.json.get('cost')
    area = request.json.get('area')
    area = Area.query.filter_by(name=area).first_or_404()
    try:
        new_chore = Chore(
            description=description,
            cost=cost,
            area_id=area.id
        )
        new_chore.insert()

    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    chore = Chore.query.filter_by(description=description).first_or_404()

    return jsonify({
        "success": True,
        "chore": chore.format()

    })


@controller_bp.route('/chores/<chore_id>', methods=['DELETE'])
def delete_chore(chore_id):
    return "Hello from the controller!"


@controller_bp.route('/chores/<chore_id>', methods=['PATCH'])
def update_chore(chore_id):
    return "Hello from the controller!"


@controller_bp.route('/areas', methods=['GET'])
def areas():
    all_areas = Area.query.all()

    if len(all_areas) == 0:
        abort(404)

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
    all_workers = Worker.query.all()

    if len(all_workers) == 0:
        abort(404)

    data = [worker.format() for worker in all_workers]

    result = {
        "success": True,
        "areas": data
    }
    return jsonify(result)


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
    all_assigned_chores = AssignedChores.query.all()

    if len(all_assigned_chores) == 0:
        abort(404)

    data = [chore.format() for chore in all_assigned_chores]

    result = {
        "success": True,
        "areas": data
    }
    return jsonify(result)


@controller_bp.route('/assigned-chores', methods=['POST'])
def assign_chore():
    return "Hello from the controller!"


@controller_bp.route('/assigned-chores/<assigned_chore_id>', methods=['DELETE'])
def delete_assigned_chore(assigned_chore_id):
    return "Hello from the controller!"


@controller_bp.route('/assigned-chores/<assigned_chore_id>', methods=['PATCH'])
def update_assigned_chore(assigned_chore_id):
    return "Hello from the controller!"


@controller_bp.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Not found"
    }), 404


@controller_bp.errorhandler(422)
def not_processable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "Can not process entity"
    }), 422


@controller_bp.errorhandler(500)
def server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Server error"
    }), 500
