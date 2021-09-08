import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Model_Owner, Car_Model, Car_Owner
from auth import AuthError, requires_auth

def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    get_models : return detail of the car models
    '''
    @app.route('/',methods=['GET'])
    def get_models():
        car_models_data = Car_Model.query.order_by(Car_Model.id).all()
        car_model = [car_model.format() for car_model in car_models_data]
        return jsonify({
            'id': car_model.id,
            'model_name': car_model.model_name
        })


    '''
    get_owners : return details of the car owners
    '''
    @app.route('/owners', methods=['GET'])
    def get_owners():
        car_owners_data = Car_Owner.query.order_by(Car_Owner.id).all()
        car_owner = [car_owner.format() for car_owner in car_owners_data]
        return jsonify({
            'id': car_owner.id,
            'owner_name': car_owner.owner_name,
            'owner_car_names': car_owner.owner_car_names,
            'purchase_date': car_owner.purchase_date

        })
    
    '''
    add_model : insert new model info into database
    '''
    @app.route('/models', methods=['POST'])
    @requires_auth('post:models')
    def add_model(model):
        body = request.get_json()
        try:
            # insert new values into database
            model_name = body.get('model_name')
            launch_date = body.get('launch_date')
            model_data = Car_Model(model_name=model_name, lauch_date = launch_date)
            model_data.insert(model_data)

            # Retrive inserted value from database
            new_model = Car_Model.query.oder_by(Car_Model.id.desc()).limit(1).first()
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
    @requires_auth('post:owners')
    def add_owner(model):
        body = request.get_json()
        try:
            # insert new values into database
            owner_name = body.get('owner_name')
            purchase_date = body.get('purchase_date')
            car_data = Car_Owner(owner_name=owner_name, purchase_date = purchase_date)
            car_data.insert(car_data)

            # Retrive inserted value from database
            new_car = Car_Owner.query.oder_by(Car_Owner.id.desc()).limit(1).first()
            new_car = new_car.format()

            return jsonify({
                'success': True,
                'model': new_car
            })
        except BaseException:
            abort(422)

        '''
    update_model:
    Create an endpoint to handle PATCH requests
    for car models.
    '''
    @app.route('/models/<int:model_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_model(model, model_id):
        body = request.get_json()
        try:
            model_name = body.get("model_name", None)
            launch_date = body.get("launch_date", None)

            # Update Actor
            model = Car_Model.query.filter(Car_Model.id == model_id).one_or_none()

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
    @ADD:
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
    @ADD: implement error handlers using the @app.errorhandler(error) decorator
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



APP = create_app()

if __name__ == '__main__':
    # APP.run(host='0.0.0.0',port=8080,debug=True)
    APP.run(host='127.0.0.1',port=8000,debug=True)