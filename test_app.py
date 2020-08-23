import unittest
import json

from flask import Flask

from model.models import Chore, Area, Worker, AssignedChore, setup_db


def setup_data():
    test_area1 = Area(name="Test Area 1")
    test_area1.insert()
    test_area2 = Area(name="Test Area 2")
    test_area2.insert()
    test_chore1 = Chore(description="Test Chore 1",
                        cost=1.2,
                        area_id="1")
    test_chore1.insert()
    test_chore2 = Chore(description="Test Chore 2",
                        cost=3.2,
                        area_id="2")
    test_chore2.insert()
    test_worker1 = Worker(name="Test Worker 1")
    test_worker1.insert()
    test_worker2 = Worker(name="Test Worker 2")
    test_worker2.insert()
    test_assigned1 = AssignedChore(chore_id=1,
                                   worker_id=1,
                                   duration="One Month",
                                   frequency="Daily")
    test_assigned1.insert()
    test_assigned2 = AssignedChore(chore_id=2,
                                   worker_id=2,
                                   duration="Two Months",
                                   frequency="Once a week")
    test_assigned2.insert()


class ChoresTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client

        self.app.config['SQLALCHEMY_DATABASE_URI'] = \
            'postgres://chores:chores@cube:5432/chores_test'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        setup_db(self.app)

        with self.app.app_context():
            from controller import controller
            self.app.register_blueprint(controller.controller_bp)

        self.WorkerToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVsZTRHWVhLRlYxS2RydVFUQnVQeSJ9.eyJpc3MiOiJodHRwczovL2Rldi03ODR5ZWMyZi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MTBiZGJmZTQ1MjcwMDZkOTNhZDhlIiwiYXVkIjoiY2hvcmVzIiwiaWF0IjoxNTk4MjA3Mjk1LCJleHAiOjE1OTgyOTM2OTUsImF6cCI6IlZtMUpIYnFhckthTFpBc2ljNktXVEtZZHJ6dDVRcFhHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YXJlYXMiLCJnZXQ6YXNzaWduZWQtY2hvcmVzIiwiZ2V0OmNob3JlcyIsImdldDp3b3JrZXJzIl19.Kiwg-ytdQJLc4_f9G7khGT-PZjoMt3cTPN0Gt1ZaVcrXpusPpOGxUrZsOwW2aiDlm-REbcrtHTbFN-SSXd2IRGU-CV6LvacHtkJURDN_-RsjZK7XxJDF6SP67WqEoUeEmIx0c1rSCP5kiZqaiukJ2Jip3gdU2fCT-oVKjCTxVMLMG1dnekHTK7lc89_gIQDDLmwVHj0azhqSuYElyR1pZY0rs05D9RlVPejFOj3XhcCDBFaHwG64O6BCDEydXKWvtg5RgDuJNjXgjVHswNL-EdAmb4QpjN0Yc3vGkyJoTjOi_uvHLKPYozAixMUxwh2F9TQnaU5PB1fz17nzrEcWYg"

        self.AdminToken = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InVsZTRHWVhLRlYxS2RydVFUQnVQeSJ9.eyJpc3MiOiJodHRwczovL2Rldi03ODR5ZWMyZi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY0MTBjMDZhMWI0MWYwMDY3ODIxMGI5IiwiYXVkIjoiY2hvcmVzIiwiaWF0IjoxNTk4MjA3MTg2LCJleHAiOjE1OTgyOTM1ODYsImF6cCI6IlZtMUpIYnFhckthTFpBc2ljNktXVEtZZHJ6dDVRcFhHIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YXJlYXMiLCJkZWxldGU6YXNzaWduZWQtY2hvcmVzIiwiZGVsZXRlOmNob3JlcyIsImRlbGV0ZTp3b3JrZXJzIiwiZ2V0OmFyZWFzIiwiZ2V0OmFzc2lnbmVkLWNob3JlcyIsImdldDpjaG9yZXMiLCJnZXQ6d29ya2VycyIsInBhdGNoOmFyZWFzIiwicGF0Y2g6YXNzaWduZWQtY2hvcmVzIiwicGF0Y2g6Y2hvcmVzIiwicGF0Y2g6d29ya2VycyIsInBvc3Q6YXJlYXMiLCJwb3N0OmFzc2lnbmVkLWNob3JlcyIsInBvc3Q6Y2hvcmVzIiwicG9zdDp3b3JrZXJzIl19.uAbxA7bjXhRo5WM78sInPHBoIlJpvlZiiOjTs0nd6LN1V15B4eGtV5EE8Xo9iMTe_9RVKgIa2L5Rh9vJeNoz2boRjUf6WVPSiaFtMj4E7gxG8Y45kYiyvmOi3uqJJCluAUsKEDuXWBqIYDNGLEw_U4_tqBIyqVVts5Rh-g6EneB8CsDLqlrcpeMPmM4iYLrRJq1ZvizjzwO8b2htVw6tNKwtz4l3p4VDyWy3I7vt5M_4Cd1PkapdJK6nboc4q-caJCqAtxe8u7ZgE17BQSQb2gLvGzEwU6gwcPtQhFh4z0w_u-VJHSeVmcPOAbQbck4gTgoAaFSMgzSa6jdFsvpe-g"

        # Setup data on first run
        # setup_data()

    def tearDown(self):
        pass

    def test_get_chores(self):
        response = \
            self.client() \
                .get('/chores',
                     headers={"Authorization": 'Bearer ' + self.AdminToken}, )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['chores'])

    def test_get_chores_with_no_jwt(self):
        response = \
            self.client() \
                .get('/chores')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_get_chores_with_worker_jwt(self):
        response = \
            self.client() \
                .get('/chores',
                     headers={"Authorization": 'Bearer ' + self.WorkerToken}, )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['chores'])

    def test_add_chore(self):
        response = self \
            .client() \
            .post('/chores',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={'description': 'Test Chore 5',
                        'cost': 1.25,
                        'area': 'Test Area 1'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_chore_no_jwt(self):
        response = self \
            .client() \
            .post('/chores',
                  json={'description': 'Test Chore 5',
                        'cost': 1.25,
                        'area': 'Test Area 1'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_add_chore_with_bad_area(self):
        response = self \
            .client() \
            .post('/chores',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={'description': 'Test Chore 6',
                        'cost': 1.25,
                        'area': 'Test Area Bad'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_chore(self):
        chore = Chore \
            .query \
            .filter(Chore.description
                    .ilike("%" + "Test Chore 5" + "%")).first()

        response = self \
            .client() \
            .delete('/chores/' + str(chore.id),
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_chore_failure(self):
        response = self \
            .client() \
            .delete('/chores/5000',
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_areas(self):
        response = self \
            .client() \
            .get('/areas',
                 headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['areas'])

    def test_get_areas_no_jwt(self):
        response = self \
            .client() \
            .get('/areas')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)

    def test_add_area(self):
        response = self \
            .client() \
            .post('/areas',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={'name': 'Test Area 5'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['area'])

    def test_add_area_with_worker_jwt(self):
        response = self \
            .client() \
            .post('/areas',
                  headers={"Authorization": 'Bearer ' + self.WorkerToken},
                  json={'name': 'Test Area 5'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)

    def test_add_area_with_no_name(self):
        response = self \
            .client() \
            .post('/areas',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_area(self):
        area = Area \
            .query \
            .filter(Area.name.ilike("%" + "Test Area 5" + "%")) \
            .first()

        response = self \
            .client() \
            .delete('/areas/' + str(area.id),
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_area_failure(self):
        response = self \
            .client() \
            .delete('/areas/5000',
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_workers(self):
        response = self \
            .client() \
            .get('/workers',
                 headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['workers'])

    def test_get_single_workers(self):
        response = self \
            .client() \
            .get('/workers/1',
                 headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['workers'])

    def test_get_single_workers_bad_request(self):
        response = self \
            .client() \
            .get('/workers/1000',
                 headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_worker(self):
        response = self \
            .client() \
            .post('/workers',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={'name': 'Test Worker 5'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['worker'])

    def test_add_worker_with_no_name(self):
        response = self \
            .client() \
            .post('/workers',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_worker(self):
        worker = Worker \
            .query \
            .filter(Worker.name.ilike("%" + "Test Worker 5" + "%")).first()

        response = self \
            .client() \
            .delete('/workers/' + str(worker.id),
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_worker_failure(self):
        response = self \
            .client() \
            .delete('/workers/5000',
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_get_assigned_chores(self):
        response = self \
            .client() \
            .get('/assigned-chores',
                 headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['chores'])

    def test_add_assigned_chores(self):
        response = self \
            .client() \
            .post('/assigned-chores',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={'chore': 'Test Chore 1',
                        'worker': 'Test Worker 2',
                        'duration': 'Test Duration',
                        'frequency': 'Test Frequency'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_assigned_chores_with_bad_worker(self):
        response = self \
            .client() \
            .post('/assigned-chores',
                  headers={"Authorization": 'Bearer ' + self.AdminToken},
                  json={'chore': 'Test Chore 1',
                        'worker': 'Test Worker 10',
                        'duration': 'Test Duration',
                        'frequency': 'Test Frequency'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_assigned_chores(self):
        chore = AssignedChore.query. \
            filter(AssignedChore
                   .duration.ilike("%" + "Test Duration" + "%")).first()

        response = self \
            .client() \
            .delete('/assigned-chores/' + str(chore.id),
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_assigned_chores_failure(self):
        response = self \
            .client() \
            .delete('/assigned-chores/5000',
                    headers={"Authorization": 'Bearer ' + self.AdminToken})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
