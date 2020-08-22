import unittest
import json

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from model.models import Chore, Area, Worker, AssignedChore, setup_db


class ChoresTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client

        # Update Database info as required to ensure testing is functional

        self.database_name = "chores_test"
        self.database_path = "postgres://{}/{}".format('chores:chores@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            from controller import controller
            self.app.register_blueprint(controller.controller_bp)

    def tearDown(self):
        pass

    def test_get_chores(self):
        response = self.client().get('/chores')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['chores'])

    def test_add_chore(self):
        response = self.client().post('/chores', json={'description': 'Test Chore 5', 'cost': 1.25, 'area': 'Test Area 1'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_chore_with_bad_area(self):
        response = self.client().post('/chores', json={'description': 'Test Chore 6', 'cost': 1.25, 'area': 'Test Area Bad'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_chore(self):
        chore = Chore.query.filter(Chore.description.ilike("%" + "Test Chore 5" + "%")).first()

        response = self.client().delete('/chores/' + str(chore.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_chore_failure(self):
        response = self.client().delete('/chores/5000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_areas(self):
        response = self.client().get('/areas')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['areas'])

    def test_add_area(self):
        response = self.client().post('/areas', json={'name': 'Test Area 5'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['area'])

    def test_add_area_with_no_name(self):
        response = self.client().post('/areas', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_area(self):
        area = Area.query.filter(Area.name.ilike("%" + "Test Area 5" + "%")).first()

        response = self.client().delete('/areas/' + str(area.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_area_failure(self):
        response = self.client().delete('/areas/5000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_workers(self):
        response = self.client().get('/workers')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['workers'])

    def test_get_single_workers(self):
        response = self.client().get('/workers/1')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['workers'])

    def test_get_single_workers_bad_request(self):
        response = self.client().get('/workers/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_worker(self):
        response = self.client().post('/workers', json={'name': 'Test Worker 5'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['worker'])

    def test_add_worker_with_no_name(self):
        response = self.client().post('/workers', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_worker(self):
        worker = Worker.query.filter(Worker.name.ilike("%" + "Test Worker 5" + "%")).first()

        response = self.client().delete('/workers/' + str(worker.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_worker_failure(self):
        response = self.client().delete('/workers/5000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_assigned_chores(self):
        response = self.client().get('/assigned-chores')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['assigned-chores'])

    def test_add_assigned_chores(self):
        response = self.client().post('/assigned-chores', json={'chore': 'Test Chore 1',
                                                                'worker': 'Test Worker 2',
                                                                'duration': 'Test Duration',
                                                                'frequency': 'Test Frequency'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_assigned_chores_with_bad_worker(self):
        response = self.client().post('/assigned-chores', json={'chore': 'Test Chore 1',
                                                                'worker': 'Test Worker 10',
                                                                'duration': 'Test Duration',
                                                                'frequency': 'Test Frequency'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_assigned_chores(self):
        chore = AssignedChore.query.filter(AssignedChore.duration.ilike("%" + "Test Duration" + "%")).first()

        response = self.client().delete('/assigned-chores/' + str(chore.id))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_assigned_chores_failure(self):
        response = self.client().delete('/assigned-chores/5000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
