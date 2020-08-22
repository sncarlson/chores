import sys

from flask import Blueprint, jsonify, abort, request
from model.models import Area, Chore, Worker, AssignedChore, db
from auth.auth import AuthError, requires_auth

# Blueprint Configuration
controller_bp = Blueprint(
    'controller_bp', __name__,
)


@controller_bp.route('/chores', methods=['GET'])
@requires_auth('get:chores')
def chores(jwt):
    all_chores = Chore.query.all()

    if len(all_chores) == 0:
        abort(404)

    data = []

    for chore in all_chores:
        record = {
            'area': chore.area.name,
            'cost': chore.cost,
            'description': chore.description
        }
        data.append(record)
    result = {
        "success": True,
        "chores": data
    }
    return jsonify(result)


@controller_bp.route('/chores', methods=['POST'])
@requires_auth('post:chores')
def create_chores(jwt):
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
@requires_auth('delete:chores')
def delete_chore(jwt, chore_id):
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
@requires_auth('patch:chores')
def update_chore(jwt, chore_id):
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
@requires_auth('get:areas')
def get_areas(jwt):
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
@requires_auth('post:areas')
def create_area(jwt):
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
@requires_auth('delete:areas')
def delete_area(jwt, area_id):
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
@requires_auth('patch:areas')
def update_area(jwt, area_id):
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
@requires_auth('get:workers')
def get_workers(jwt):
    all_workers = Worker.query.all()

    if len(all_workers) == 0:
        abort(404)

    data = []

    for worker in all_workers:
        record = {
            'name': worker.name
        }
        data.append(record)

    result = {
        "success": True,
        "workers": data
    }
    return jsonify(result)


@controller_bp.route('/workers/<worker_id>', methods=['GET'])
@requires_auth('get:workers')
def get_single_worker(jwt, worker_id):
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
        'name': worker.name,
        'chores': worker_chores
    }
    data.append(record)

    result = {
        "success": True,
        "workers": data
    }
    return jsonify(result)


@controller_bp.route('/workers', methods=['POST'])
@requires_auth('post:workers')
def create_worker(jwt):
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
@requires_auth('delete:workers')
def delete_worker(jwt, worker_id):
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
@requires_auth('patch:workers')
def update_worker(jwt, worker_id):
    error = False
    try:
        worker = Worker.query.filter_by(id=worker_id).first_or_404()
        if request.json.get('name') == "":
            abort(422)

        if request.json.get('name'):
            worker.name = request.json.get('name')

        worker.update()
        worker = Worker.query.filter_by(id=worker_id).first_or_404()

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
@requires_auth('get:assigned-chores')
def assigned_chores(jwt):
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
        "chores": data
    }
    return jsonify(result)


@controller_bp.route('/assigned-chores', methods=['POST'])
@requires_auth('post:assigned-chores')
def assign_chore(jwt):
    chore = request.json.get('chore')
    chore = Chore.query.filter_by(description=chore).first_or_404()
    worker = request.json.get('worker')
    worker = Worker.query.filter_by(name=worker).first_or_404()
    duration = request.json.get('duration')
    frequency = request.json.get('frequency')

    try:
        new_assigned_chore = AssignedChore(
            chore_id=chore.id,
            worker_id=worker.id,
            duration=duration,
            frequency=frequency
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
@requires_auth('delete:assigned-chores')
def delete_assigned_chore(jwt, assigned_chore_id):
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
@requires_auth('patch:assigned-chores')
def update_assigned_chore(jwt, assigned_chore_id):
    error = False
    try:
        assigned_chore = AssignedChore.query.filter_by(id=assigned_chore_id).first_or_404()
        if request.json.get('worker') == "" or request.json.get('chore') == "" or request.json.get(
                'duration') == "" or request.json.get('frequency') == "":
            abort(422)

        if request.json.get('worker'):
            worker = Worker.query.filter_by(name=request.json.get('worker')).first_or_404()
            assigned_chore.worker_id = worker.id

        if request.json.get('chore'):
            chore = Chore.query.filter_by(description=request.json.get('chore')).first_or_404()
            assigned_chore.chore_id = chore.id

        if request.json.get('duration'):
            assigned_chore.duration = request.json.get('duration')

        if request.json.get('frequency'):
            assigned_chore.frequency = request.json.get('frequency')

        assigned_chore.update()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()

    assigned_chore = AssignedChore.query.filter_by(id=assigned_chore_id).first_or_404()
    data = []

    record = {
        'chore': assigned_chore.chore.description,
        'area': assigned_chore.chore.area.name,
        'wage': assigned_chore.chore.cost,
        'worker': assigned_chore.worker.name,
        'duration': assigned_chore.duration,
        'frequency': assigned_chore.frequency
    }
    data.append(record)

    if error:
        abort(500)
    else:
        return jsonify({
            "success": True,
            "chores": data
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


@controller_bp.errorhandler(401)
def invalid_token(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "Token expired or incorrect claim."
    }), 401


@controller_bp.errorhandler(400)
def invalid_header(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Invalid header"
    }), 400


@controller_bp.errorhandler(403)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "Unauthorized"
    }), 403


@controller_bp.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response
