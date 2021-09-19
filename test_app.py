import os
import unittest
import json
import urllib.request
from flask import Flask, request, _request_ctx_stack, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from app import create_app
from models import setup_db, Model_Owner, Car_Model, Car_Owner
from auth import AuthError, requires_auth
from data_csv import Car_Data


class ATRCarTestCase(unittest.TestCase):
    """ This class represents ATRCar test case """

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_TEST_URL']
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        # Create New Model
        self.new_model = {
            'model_name': 'Honda Elite',
            'launch_date': '1997-07-25'
        }

        # Create New Owner
        self.new_owner = {
            'owner_name': 'Sophy cruise',
            'address': '1123 Rosamud Dr, Fremont, 94582'
        }

        self.atrcar_director_jwt = {
            'Authorization': "Bearer $DIRECTOR_TOKEN"
        }
        self.atrcar_manager_jwt = {
            'Authorization': "Bearer $MANAGER_TOKEN"
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Write at least one test for each test for successful operation
    and for expected errors.
    """

    # Run test to get Models and Error occures

    def test_get_models(self):
        res = self.client().get('/models')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['models'])

    def test_405_if_model_not_found(self):
        res = self.client().get('/models/35')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to get Owners and Error occures

    def test_get_owners(self):
        res = self.client().get('/owners')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['owners'])

    def test_405_if_owner_not_found(self):
        res = self.client().get('/owners/100')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to add Model and Error occures

    def test_add_new_model(self):
        res = self.client().post('/models', json=self.new_model,
                                 headers=self.atrcar_director_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['model'])
        self.assertTrue(len(data['model']))

    def test_405_if_model_addition_not_allowed(self):
        res = self.client().post('/models/45', json=self.new_model,
                                 headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test for Role base atrcar_manager doesn't
    # have permission to add Model
    def test_unauthorize_for_add_new_model(self):
        res = self.client().post('/models', json=self.new_model,
                                 headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    # Run test to add Owner and Error occurs

    def test_add_new_owner(self):
        res = self.client().post('/owners', json=self.new_owner,
                                 headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['owner'])
        self.assertTrue(len(data['owner']))

    def test_405_if_owner_addition_not_allowed(self):
        res = self.client().post('/owners/122', json=self.new_owner,
                                 headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Run test to update Model and Error occures

    def test_update_model_name(self):
        res = self.client().patch(
            'models/8', json={'model_name': 'Honda City'},
            headers=self.atrcar_director_jwt
        )
        data = json.loads(res.data)
        model = Car_Model.query.filter(Car_Model.id == 8).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(model.format()['model_name'], 'Honda City')

    def test_400_for_failed_model_update(self):
        res = self.client().patch(
            '/models/101', headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test to assign Models to the Owner

    def test_assign_models_to_owner(self):
        res = self.client().patch(
            'owners/6',
            json={
                'selected_models': [
                    '10',
                    '11']},
            headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        owner_models = Model_Owner.query.filter(
            Model_Owner.owner_id == 6).all()
        selected_models = []
        if owner_models:
            selected_models = [str(owner_model.model_id)
                               for owner_model in owner_models]

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(selected_models, ['10', '11'])

    # Run test to update Owner and Error occurs

    def test_update_owner_name(self):
        res = self.client().patch(
            '/owners/4', json={'owner_name': 'Purvi Rawal'},
            headers=self.atrcar_manager_jwt
        )
        data = json.loads(res.data)
        owner = Car_Owner.query.filter(Car_Owner.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(owner.format()['owner_name'], 'Purvi Rawal')

    def test_400_for_failed_owner_update(self):
        res = self.client().patch('owners/1000',
                                  json={'owner_name': 'Purvi Rawal'},
                                  headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test to delete Model and Error occures

    def test_delete_model(self):
        res = self.client().delete(
            'models/5', headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        model = Car_Model.query.filter(Car_Model.id == 5).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 5)
        self.assertEqual(model, None)

    def test_400_if_model_does_not_exit(self):
        res = self.client().delete(
            '/models/1000', headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test for Role base atrcar manager doesn't
    # have permission to delete model

    def test_unauthorize_for_delete_model(self):
        res = self.client().delete('/models/3',
                                   headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    # Run Test to delete Owner and Error occurs

    def test_delete_owner(self):
        res = self.client().delete('owners/2', headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        owner = Car_Owner.query.filter(Car_Owner.id == 2).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        self.assertEqual(owner, None)

    def test_400_if_owner_does_not_exit(self):
        res = self.client().delete('owners/4000',
                                   headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Run test for read model CSV file and store data
    # into database and Error occurs

    def test_read_model_csv_into_database(self):
        res = self.client().get('model_csv_to_db/models.csv',
                                headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['car_models'])
        self.assertTrue(len(data['car_models']))

    def test_404_if_model_csv_dose_not_exist(self):
        res = self.client().get('models/model_csv_to_do',
                                headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Run test for read Owner CSV file and store data
    # into database and Error occurs

    def test_read_owner_csv_into_database(self):
        res = self.client().get('owner_csv_to_db/owners.csv',
                                headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['car_owners'])
        self.assertTrue(len(data['car_owners']))

    def test_404_if_owner_csv_dose_not_exist(self):
        res = self.client().get('owners/owner_csv_to_db',
                                headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Run test for wirte Model CSV file from Database information

    def test_write_model_csv_from_database(self):
        res = self.client().get('/db_to_model_csv/test_models.csv',
                                headers=self.atrcar_director_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'],
            'Model information from database store in test_models.csv'
        )

    # Run test for Role base atrcar manager doesn't have
    # permission to write csv for model information

    def test_unauthorize_for_write_model_csv(self):
        res = self.client().get('/db_to_model_csv/models.csv',
                                headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['description'],
                         'Permission not found.')

    # Run test for wirte Owner CSV file from Database information

    def test_write_owner_csv_from_database(self):
        res = self.client().get('/db_to_owner_csv/test_owners.csv',
                                headers=self.atrcar_manager_jwt)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(
            data['message'],
            'Owner information from database store in test_owners.csv'
        )

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
