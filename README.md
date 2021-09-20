# ATRCar-API

The ATRCar is a Car Dealer Company that is responsible for launch new car Model and managing and deliver Model to Customer. There are two users Company Director and Comapny Manager within the company and are creating a system to simplify and streamline this process.

The ATRCar code follows PEP8 style guidelines.

### Agency Tasks:
1) Display models and owners list with details.
2) Allow Company Manager to add, delete Owners and edit Model and Owner details.
3) Allow Company Director to create, delete Models and all the permissoins that Comapny Manager has. 

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is library to handle the database. Model file can be found in `models.py`. 

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Database Setup
With Postgres running, restore a database using the atrcar.psql file provided. From the folder in terminal run:
```bash
psql atrcar < atrcar.psql
```

## Testing
To run the tests, run
```
dropdb atrcar_test
createdb atrcar_test
psql atrcar_test < atrcar.psql
python3 test_app.py
```

## Running the server

From within the directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `delete:owner`
    - `delete:model`
    - `get:owner`
    - `get:model`
    - `patch:owner`
    - `patch:model`
    - `post:owner`
    - `post:model`
6. Create new roles for:
    - Company Manage
        - can perform all actions except `post:model` and `delete:model`
    - Company Director
        - can perform all actions

## Endpoints:

1. Get Owners

    GET '/owners'
    - Fetches all actors with detail: id, owner_name, address, owner_car_names.
    - Request Arguments: None
    - Returns: An object owners with all the owners with id, owner_name, address, owner_car_names.
    - curl https://atrcar-api.herokuapp.com/actors
    - {
        "owners": [
        {
            "id": 1,
            "owner_name": "Purvi Rawal"
            "address": "1123 Rosamund Drive, San Carlos, 95862", 
            "owner_car_names": [
              "City", 
              "Insight"
            ], 
        }, 
        :
        :
        :
        ],
        "success":true
     }

2. Post Owner

    POST '/owners'
    - Insert owner into database with detail: owner_name, adress.
    - Request Arguments: owner
    - Returns: An object actors with all the actors with id, owner_name, adress.
    - curl -X POST  -H "Content-Type:application/json" -H "Authorization: Bearer $MANAGER_TOKEN" https://atrcar-api.herokuapp.com/owners 
       -d '{"owner_name":"Kristin Stewart","adress":"39210 State St suite 205, Fremont, CA 94582"}'
    - {
        "owner":{
            "adress":"39210 State St suite 205, Fremont, CA 94582",
            "id":17,
            "owner_name":"Kristin Stewart",
            "owner_car_names": [] 
        },
        "success":true
      }

3. Update Owner

    PATCH '/owners/<int:owner_id>'
    - Update owner's detail.
    - Request Arguments: owner_id
    - Returns: An object owner with id, owner_name, adress, owner_car_names.
    - curl -X PATCH https://atrcar-api.herokuapp.com/owners/8 -H"Content-Type: application/json" -H "Authorization: Bearer $MANAGER_TOKEN"
       -d '{"owner_name":"Angie"}'
    - {
        "owner":[
            {
                "id":8,
                "owner_name":"Angie",
                "address":"3315 Casa Grande Dr, San Ramon, CA 94583"
                "owner_car_names":[]
            }
        ]
        ,"success":true
      }

4. Delete Owner

    DELETE '/owners/<int:owner_id>'
    - Delete owner from owners and model_owner table.
    - Request Arguments: owner_id
    - Returns: An object delete with owner_id.
    - curl -X DELETE  -H "Content-Type:application/json" -H 
       "Authorization:Bearer $MANAGER_TOKEN" 
       https://atrcar-api.herokuapp.com/owners/15
    - {
        "success": True,
        "delete": 15
      }

5. Get Models

    GET '/models'
    - Fetches all movies with detail: id, launch_date, model_name.
    - Request Arguments: None
    - curl https://atrcar-api.herokuapp.com/models
    - {
        "models": [
            {
              "id": 1, 
              "launch_date": "Monday, 10 December 2018", 
              "model_name": "Accord"
            }, 
            :
            :
            :
        ],
        "success":true
      }

6. POST Model

    POST '/models'
    - Insert model into database with detail: model_name, launch_date.
    - Request Arguments: model
    - Returns: An object actors with all the actors with id, model_name, launch_date.
    - curl -X POST  -H "Content-Type:application/json" -H "Authorization:
             Bearer $DIRECTOR_TOKEN" https://atrcar-api.herokuapp.com/movies
             -d '{"model_name":"Honda City", "launch_date": "10/12/2018"}'
    - {
        "model":[
            {
                "id": 17, 
                "launch_date": "Monday, 10 December 2018", 
                "model_name": "Accord"
            },
        ],
        "success":true
      }

7. Assign model to the owner

    PATCH '/owners/<int:owner_id>'
    - Assign model to the Owner. Insert value to the model_owner table.
    - Request Arguments: owner_id
    - Returns: An object owner with detais: id, owner_name, address, owner_car_names.
    - curl -X PATCH https://atrcar-api.herokuapp.com/owners/16 -H 
       "Content-Type: application/json" -H "Authorization: Bearer $DIRECTOR_TOKEN" 
       -d '{"selected_models":["8","9"]}'
    - {
        owners": [
          {
            "address": "2057 Elderberry Drive, San Ramon, 94582", 
            "id": 1, 
            "owner_car_names": [
              "City", 
              "Insight"
            ], 
            "owner_name": "Purvi Rawal"
          }, 
        ],
        "success":true
      }

8. Delete Model

    DELETE '/model/<int:model_id>'
    - Delete model from model and model_owner table.
    - Request Arguments: model_id
    - Returns: An object delete with model_id.
    - curl -X DELETE  -H "Content-Type:application/json" -H "Authorization:Bearer
       $PRODUCER_TOKEN" https://atrcar-api.herokuapp.com/movies/18
    - {
        "success": True,
        "delete": 18
      }
    

9. Read Model CSV store information into Database.

    GET '/model_csv_to_db/<file_name>'
    - Insert model information from models.csv into models table.
    - Request Arguments: file_name
    - Returns: An object car_models.
    - curl -X GET  -H "Content-Type:application/json" -H "Authorization:Bearer
       $DIRECTOR_TOKEN" https://atrcar-api.herokuapp.com/model_csv_to_db/models.csv
    - {
        "car_models": [
          {
            "id": 1, 
            "launch_date": "Monday, 10 December 2018", 
            "model_name": "Accord"
          }, 
          {
            "id": 2, 
            "launch_date": "Saturday, 03 March 2012", 
            "model_name": "City"
          }
          :
          :
          :
          ], 
          "success": true
      }
      
9. Read Owner CSV store information into Database.

    GET '/owner_csv_to_db/<file_name>'
    - Insert owner information from owners.csv into owners table.
    - Request Arguments: file_name
    - Returns: An object car_owners.
    - curl -X GET  -H "Content-Type:application/json" -H "Authorization:Bearer
       $MANAGER_TOKEN" https://atrcar-api.herokuapp.com/owner_csv_to_db/owners.csv
    - {
        "car_owners": [
          {
            "address": "2057 Elderberry Drive, San Ramon, 94582", 
            "id": 1, 
            "owner_car_names": [
                "City", 
                "Insight"
            ], 
            "owner_name": "Purvi Rawal"
          }, 
          {
            "address": "2057 Elderberry Drive, San Ramon, 94582", 
            "id": 2, 
            "owner_car_names": [
              "Accord", 
              "City"
            ], 
            "owner_name": "Tushar Rawal"
          }, 
          :
          :
          :
          ], 
          "success": true
      }      

10. Write Model CSV from Database information.

    GET '/db_to_model_csv/<file_name>'
    - Write owner information from models database into models.csv .
    - Request Arguments: file_name
    - Returns: An message object.
    - curl -X GET  -H "Content-Type:application/json" -H "Authorization:Bearer
       $DIRECTOR_TOKEN" https://atrcar-api.herokuapp.com/db_to_model_csv/models.csv
    - {
        "message": "Model information from database store in models.csv", 
        "success": true
      }

10. Write Onwer CSV from Database information.

    GET '/db_to_owner_csv/<file_name>'
    - Write owner information from owners database into owners.csv .
    - Request Arguments: file_name
    - Returns: An message object.
    - curl -X GET  -H "Content-Type:application/json" -H "Authorization:Bearer
       $DIRECTOR_TOKEN" https://atrcar-api.herokuapp.com/db_to_owner_csv/owners.csv
    - {
        "message": "Owner information from database store in owners.csv", 
        "success": true
      }
      
## Error Handling

    Errors are returned as JSON objects in the following format:
    {
        "error": 404, 
        "message": "resource not found", 
        "success": false
    }

    The API will return six types of error when requests fail:

    1. 400: Bad Request
    2. 401: Authorization Error
    3. 404: Resource Not Found
    4. 405: Method Not Allowed
    5. 422: Unprocessable
    6. 500: Internal Server Error

### The Server

Files are used to work the server.
1. `auth.py`
2. `app.py`
3. `models.py`
4. `data_csv.py`

### Deployment
**ATRCar-API** application deployed in **_Heroku_**. This is the url for [**ATRCar**](https://atrcar-api.herokuapp.com/models).

### Author
Purvi Rawal

### Acknoledgemnts
[**Stack Overflow**](https://stackoverflow.com/) and [**Python Documentation**](https://docs.python.org/3/)
