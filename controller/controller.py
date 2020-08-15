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

from flask import Blueprint, jsonify, abort, request
from model.models import Area, Chore, Worker, AssignedChore, db

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
        "chores": data
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
    error = False

    chore = Chore.query.filter_by(id=chore_id).first_or_404()
    try:
        chore.delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "delete": chore_id
        })


@controller_bp.route('/chores/<chore_id>', methods=['PATCH'])
def update_chore(chore_id):
    error = False
    try:
        chore = Chore.query.filter_by(id=chore_id).first_or_404()
        if request.json.get('description') == "" or request.json.get('cost') == "" or request.json.get('area') == "":
            abort(422)

        if request.json.get('description'):
            chore.description = request.json.get('description')

        if request.json.get('cost'):
            chore.cost = request.json.get('cost')

        if request.json.get('area'):
            area = Area.query.filter_by(name=request.json.get('area')).first_or_404()
            chore.area_id = area.id

        chore.update()
        chore = Chore.query.filter_by(id=chore_id).first_or_404()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "chores": [chore.format()]
        })


@controller_bp.route('/areas', methods=['GET'])
def get_areas():
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
    name = request.json.get('name')
    try:
        new_area = Area(
            name=name
        )
        new_area.insert()

    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    area = Area.query.filter_by(name=name).first_or_404()

    return jsonify({
        "success": True,
        "area": area.format()

    })


@controller_bp.route('/areas/<area_id>', methods=['DELETE'])
def delete_area(area_id):
    error = False

    area = Area.query.filter_by(id=area_id).first_or_404()
    try:
        area.delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "delete": area_id
        })


@controller_bp.route('/areas/<area_id>', methods=['PATCH'])
def update_area(area_id):
    error = False
    try:
        area = Area.query.filter_by(id=area_id).first_or_404()
        if request.json.get('name') == "":
            abort(422)

        if request.json.get('name'):
            area.name = request.json.get('name')

        area.update()
        area = Area.query.filter_by(id=area_id).first_or_404()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "areas": [area.format()]
        })


@controller_bp.route('/workers', methods=['GET'])
def get_workers():
    all_workers = Worker.query.all()

    if len(all_workers) == 0:
        abort(404)

    data = []

    for worker in all_workers:
        worker_chores = []
        for worker_chore in worker.assigned_chores:
            chore_record = {
                'description': worker_chore.chore.description,
                'area': worker_chore.chore.area.name,
                'wage': worker_chore.chore.cost,
                'frequency': worker_chore.frequency,
                'duration': worker_chore.duration
            }
            worker_chores.append(chore_record)
        record = {
            'name:': worker.name,
            'chores': worker_chores
        }
        data.append(record)

    result = {
        "success": True,
        "workers": data
    }
    return jsonify(result)


@controller_bp.route('/workers/<worker_id>', methods=['GET'])
def get_single_worker(worker_id):
    worker = Worker.query.filter_by(id=worker_id).first_or_404()

    data = []

    worker_chores = []
    for worker_chore in worker.assigned_chores:
        chore_record = {
            'description': worker_chore.chore.description,
            'area': worker_chore.chore.area.name,
            'wage': worker_chore.chore.cost,
            'frequency': worker_chore.frequency,
            'duration': worker_chore.duration
        }
        worker_chores.append(chore_record)
    record = {
        'name:': worker.name,
        'chores': worker_chores
    }
    data.append(record)

    result = {
        "success": True,
        "workers": data
    }
    return jsonify(result)


@controller_bp.route('/workers', methods=['POST'])
def create_worker():
    name = request.json.get('name')
    try:
        new_worker = Worker(
            name=name
        )
        new_worker.insert()

    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    worker = Worker.query.filter_by(name=name).first_or_404()

    return jsonify({
        "success": True,
        "worker": worker.format()
    })


@controller_bp.route('/workers/<worker_id>', methods=['DELETE'])
def delete_worker(worker_id):
    error = False

    worker = Worker.query.filter_by(id=worker_id).first_or_404()
    try:
        worker.delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "delete": worker_id
        })


@controller_bp.route('/workers/<worker_id>', methods=['PATCH'])
def update_worker(worker_id):
    error = False
    try:
        worker = Worker.query.filter_by(id=worker_id).first_or_404()
        if request.json.get('name') == "":
            abort(422)

        if request.json.get('name'):
            worker.name = request.json.get('name')

        worker.update()
        worker = Area.query.filter_by(id=worker_id).first_or_404()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "worker": [worker.format()]
        })


@controller_bp.route('/assigned-chores', methods=['GET'])
def assigned_chores():
    all_assigned_chores = AssignedChore.query.all()

    if len(all_assigned_chores) == 0:
        abort(404)

    data = []

    for chore in all_assigned_chores:
        record = {
            'chore': chore.chore.description,
            'area': chore.chore.area.name,
            'wage': chore.chore.cost,
            'worker': chore.worker.name,
            'duration': chore.duration,
            'frequency': chore.frequency
        }
        data.append(record)

    result = {
        "success": True,
        "assigned-chores": data
    }
    return jsonify(result)


@controller_bp.route('/assigned-chores', methods=['POST'])
def assign_chore():
    chore = request.json.get('chore')
    chore = Chore.query.filter_by(description=chore).first_or_404()
    worker = request.json.get('worker')
    worker = Worker.query.filter_by(name=worker).first_or_404()

    try:
        new_assigned_chore = AssignedChore(
            chore_id=chore.id,
            worker_id=worker.id,
            complete=False
        )
        new_assigned_chore.insert()

    except:
        print(sys.exc_info())
    finally:
        db.session.close()

    return jsonify({
        "success": True
    })


@controller_bp.route('/assigned-chores/<assigned_chore_id>', methods=['DELETE'])
def delete_assigned_chore(assigned_chore_id):
    error = False

    chore = AssignedChore.query.filter_by(id=assigned_chore_id).first_or_404()
    try:
        chore.delete()
        db.session.commit()
    except:
        error = True
        db.session.rollback()
        print(sys.exe_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "delete": assigned_chore_id
        })


@controller_bp.route('/assigned-chores/<assigned_chore_id>', methods=['PATCH'])
def update_assigned_chore(assigned_chore_id):
    error = False
    try:
        assigned_chore = AssignedChore.query.filter_by(id=assigned_chore_id).first_or_404()
        if request.json.get('worker') == "" or request.json.get('chore') == "":
            abort(422)

        if request.json.get('worker'):
            worker = Worker.query.filter_by(name=request.json.get('worker')).first_or_404()
            assigned_chore.worker_id = worker.id

        if request.json.get('chore'):
            chore = Chore.query.filter_by(description=request.json.get('chore')).first_or_404()
            assigned_chore.chore_id = chore.id

        assigned_chore.update()
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True
        })


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
