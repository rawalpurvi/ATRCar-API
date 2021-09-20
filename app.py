import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


from models import setup_db, Model_Owner, Car_Model, Car_Owner
from auth import AuthError, requires_auth
from data_csv import Car_Data


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    get_api:
    Create an endpoint to handle GET request
    for API.
    '''
    # API Start
    @app.route('/', methods=['GET'])
    def get_api():
        # Put Message
        message = "This is the ATRCar API!!!"
        # retrun message
        return jsonify({
            'success': True,
            'message': message
        })

    '''
    get_models : return detail of the car models
    '''
    @app.route('/models', methods=['GET'])
    def get_models():
        car_models_data = Car_Model.query.order_by(Car_Model.id).all()
        car_model = [car_model.format() for car_model in car_models_data]

        # if there is no model added
        if len(car_model) == 0:
            abort(404)

        # Return model information
        return jsonify({
            'success': True,
            'models': car_model
        })

    '''
    get_owners : return details of the car owners
    '''
    @app.route('/owners', methods=['GET'])
    def get_owners():
        car_owners_data = Car_Owner.query.order_by(Car_Owner.id).all()
        car_owner = [car_owner.format() for car_owner in car_owners_data]

        # if there is no owner added
        if len(car_owner) == 0:
            abort(404)

        # Return owner information
        return jsonify({
            'success': True,
            'owners': car_owner
        })

    '''
    add_model : insert new model info into database
    '''
    @app.route('/models', methods=['POST'])
    @requires_auth('post:model')
    def add_model(model):
        body = request.get_json()
        try:
            # insert new values into database
            model_name = body.get('model_name')
            launch_date = body.get('launch_date')

            model_data = Car_Model(model_name=model_name,
                                   launch_date=launch_date)
            model_data.insert()

            # Retrive inserted value from database
            new_model = Car_Model.query.order_by(
                Car_Model.id.desc()).limit(1).first()
            new_model = new_model.format()

            return jsonify({
                'success': True,
                'model': new_model
            })
        except BaseException:
            abort(422)

    '''
    add_owner : insert new owner info into database
    '''
    @app.route('/owners', methods=['POST'])
    @requires_auth('post:owner')
    def add_owner(owner):
        body = request.get_json()
        try:
            # insert new values into database
            owner_name = body.get('owner_name')
            address = body.get('address')
            car_data = Car_Owner(owner_name=owner_name, address=address)
            car_data.insert()

            # Retrive inserted value from database
            new_owner = Car_Owner.query.order_by(
                Car_Owner.id.desc()).limit(1).first()
            new_owner = new_owner.format()

            return jsonify({
                'success': True,
                'owner': new_owner
            })
        except BaseException:
            abort(422)

    '''
    update_model:
    Create an endpoint to handle PATCH requests
    for car models.
    '''
    @app.route('/models/<int:model_id>', methods=['PATCH'])
    @requires_auth('patch:model')
    def update_model(model, model_id):
        body = request.get_json()
        try:
            model_name = body.get("model_name", None)
            launch_date = body.get("launch_date", None)

            # Update Actor
            model = Car_Model.query.filter(
                Car_Model.id == model_id).one_or_none()

            if model is None:
                abort(404)

            if model_name:
                model.model_name = model_name
            if launch_date:
                model.launch_date = launch_date

            model.update()
            updated_model = model.format()

            return jsonify({
                'success': True,
                'model': [updated_model]
            })

        except BaseException:
            abort(400)

    '''
    update_owner:
    Create an endpoint to handle PATCH requests
    for car owners.
    '''
    @app.route('/owners/<int:owner_id>', methods=['PATCH'])
    @requires_auth('patch:owner')
    def update_owner(owner, owner_id):
        body = request.get_json()

        try:
            owner_name = body.get("owner_name", None)
            address = body.get("address", None)
            model_ids = body.get("selected_models", None)

            # Check models are already assigned
            owner_models = Model_Owner.query.filter(
                Model_Owner.owner_id == owner_id).all()

            if owner_models:
                for owner_model in owner_models:
                    owner_model.delete()

            # Set updated movie id and actor id in movie_actor table
            if model_ids:
                for model_id in model_ids:
                    model_owner = Model_Owner(
                        model_id=model_id, owner_id=owner_id)
                    model_owner.insert()

            # Update Owner
            owner = Car_Owner.query.filter(
                Car_Owner.id == owner_id).one_or_none()

            if owner is None:
                abort(404)

            if owner_name:
                owner.owner_name = owner_name
            if address:
                owner.address = address

            owner.update()
            updated_owner = owner.format()

            return jsonify({
                'success': True,
                'owner': [updated_owner]
            })

        except BaseException:
            abort(400)

    '''
    delete_model:
    Create an endpoint to handle DELETE requests
    for models.
    '''
    @app.route('/models/<int:model_id>', methods=['DELETE'])
    @requires_auth('delete:model')
    def delete_model(model, model_id):

        try:
            # Delete Model
            model = Car_Model.query.filter(
                Car_Model.id == model_id).one_or_none()
            if model is None:
                abort(404)

            model.delete()

            return jsonify({
                'success': True,
                'delete': model_id
            })

        except BaseException:
            abort(400)

    '''
    delete_owner:
    Create an endpoint to hande DELETE requets for owners.
    '''
    @app.route('/owners/<int:owner_id>', methods=['DELETE'])
    @requires_auth('delete:owner')
    def delete_owner(owner, owner_id):

        # Delete Owner
        try:
            owner = Car_Owner.query.filter(
                Car_Owner.id == owner_id).one_or_none()
            if owner is None:
                abort(404)

            owner.delete()

            return jsonify({
                'success': True,
                'delete': owner_id
            })

        except BaseException:
            abort(400)

    '''
    model_csv_to_database: Store Model information from CSV file into Database.
    '''
    @app.route('/model_csv_to_db/<file_name>', methods=['GET'])
    @requires_auth('post:model')
    def model_csv_to_database(model, file_name):
        if os.path.exists('readCSV/{}'.format(file_name)):
            try:
                car_models = Car_Data('readCSV/models.csv')
                models = car_models.read_model_csv()
                if models:
                    for model in models:
                        add_model = Car_Model(
                            model_name=model['model_name'],
                            launch_date=model['launch_date']
                        )
                        add_model.insert()
                return jsonify({
                    'success': True,
                    'car_models': models
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

    '''
    owner_csv_to_database: Store Owner information from CSV file into Database.
    '''
    @app.route('/owner_csv_to_db/<file_name>', methods=['GET'])
    @requires_auth('post:owner')
    def owner_csv_to_database(owner, file_name):
        if os.path.exists('readCSV/{}'.format(file_name)):
            try:
                car_owners = Car_Data('readCSV/{}'.format(file_name))
                owners = car_owners.read_owner_csv()
                if owners:
                    for owner in owners:
                        add_owner = Car_Owner(
                            owner_name=owner['owner_name'],
                            address=owner['address']
                        )
                        add_owner.insert()
                return jsonify({
                    'success': True,
                    'car_owners': owners
                })
            except BaseException:
                abort(422)
        else:
            abort(404)

    '''
    database_to_model_csv: Store Model information from CSV file into Database.
    '''
    @app.route('/db_to_model_csv/<file_name>', methods=['GET'])
    @requires_auth('post:model')
    def database_to_model_csv(model, file_name):
        try:
            model_data = Car_Model.query.order_by(Car_Model.id).all()
            models = [model.format() for model in model_data]
            if models:
                car_models = Car_Data('writeCSV/{}'.format(file_name))
                car_models.write_model_csv(models)
                return jsonify({
                    'success': True,
                    'message':
                    'Model information from database store in {}'
                    .format(file_name)
                })
            else:
                abort(404)
        except BaseException:
            abort(422)

    '''
    database_to_model_csv: Store Owner information from CSV file into Database.
    '''
    @app.route('/db_to_owner_csv/<file_name>', methods=['GET'])
    @requires_auth('post:owner')
    def database_to_owner_csv(owner, file_name):
        try:
            owner_data = Car_Owner.query.order_by(Car_Owner.id).all()
            owners = [owner.format() for owner in owner_data]
            if owners:
                car_owners = Car_Data('writeCSV/{}'.format(file_name))
                car_owners.write_owner_csv(owners)
                return jsonify({
                    'success': True,
                    'message':
                    'Owner information from database store in {}'
                    .format(file_name)
                })
            else:
                abort(404)
        except BaseException:
            abort(422)

    '''
    errorhandler:
    Error Handling
    '''
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": " A generic error occurred on the server"
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'method not allowed'
        }), 405

    '''
    handle_auth_error:
        implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
    '''
    @app.errorhandler(AuthError)
    def handle_auth_error(ex):
        return jsonify({
            "success": False,
            "error": ex.status_code,
            "message": ex.error
        }), ex.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=os.environ['PORT'], debug=True)
    #app.run(host='127.0.0.1', port=5000, debug=True)
