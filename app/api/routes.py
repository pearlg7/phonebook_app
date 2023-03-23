from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, car_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    vin = request.json['vin']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(vin, make, model, year, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response = car_schema.dump(car)
    return jsonify(response)

@api.route('/contacts', methods = ['GET'])
@token_required
def get_car(current_user_token):
    a_user = current_user_token.token
    car = Car.query.filter_by(user_token = a_user).all()
    response = car_schema.dump(car)
    return jsonify(response)


@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_string_car(current_user_token, id):
    car = Car.query.get(id)
    response = car_schema.dump(car)
    return jsonify(response)
    

 # Updating endpoint
@api.route('/car/<id>', methods = ['POST', 'PUT'])
@token_required
def update_car(current_user_token, id):
    car = Car.query.get(id)
    car.vin = request.json['vin']
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.user_toke4n = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
    

# Delete endpoint
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)