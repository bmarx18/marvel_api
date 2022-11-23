from flask import Blueprint, request, jsonify
from marvel_comics.helpers import token_required
from marvel_comics.models import db, Avenger, avenger_schema, avengers_schema

api = Blueprint('api', __name__, url_prefix = '/api')

@api.route('/getdata')
@token_required
def getdata(current_user_data):
    return { 'some': 'value' }

@api.route('/avengers', methods = ['POST'])
@token_required
def create_avenger(current_user_token):
    name = request.json['name']
    power_abilities = request.json['power_abilities']
    height = request.json['height']
    movies = request.json['movies']
    comics = request.json['comics']
    allies = request.json['allies']
    enemies = request.json['enemies']
    groups = request.json['groups']
    living_or_decease = request.json['living_or_decease']
    user_token = current_user_token.token

    print(f'User Token: {current_user_token.token}')

    avenger = Avenger(name, power_abilities, height, movies, comics, allies, enemies, groups, living_or_decease, 
    user_token = user_token)

    db.session.add(avenger)
    db.session.commit()

    response = avenger_schema.dump(avenger)

    return jsonify(response)

@api.route('/avengers', methods = ['GET'])
@token_required
def get_avengers(current_user_token):
    owner = current_user_token.token
    avengers = Avenger.query.filter_by(user_token = owner).all()
    response = avengers_schema.dump(avengers)
    return jsonify(response)

@api.route('/avengers/<id>', methods = ['GET'])
@token_required
def get_avenger(current_user_token, id):
    owner = current_user_token
    if owner == current_user_token.token:
        avenger = Avenger.query.get(id)
        response = avenger_schema.dump(avenger)
        return jsonify(response)
    else:
        return jsonify({ 'message': 'Valid Token Required' }), 401

@api.route('/avengers/<id>', methods = ['POST', 'PUT'])
@token_required
def update_avenger(current_user_token, id):
    avenger = Avenger.query.get(id)
    avenger.name = request.json['name']
    avenger.power_abilities = request.json['power_abilities']
    avenger.height = request.json['height']
    avenger.movies = request.json['movies']
    avenger.comics = request.json['comics']
    avenger.allies = request.json['allies']
    avenger.enemies = request.json['enemies']
    avenger.groups = request.json['groups']
    avenger.living_or_decease = request.json['living_or_decease']
    avenger.user_token = current_user_token.token

    db.session.commit()
    response = avenger_schema.dump(avenger)
    return jsonify(response)


@api.route('/avengers/<id>', methods = ["DELETE"])
@token_required
def delete_avenger(current_user_token, id):
    avenger = Avenger.query.get(id)
    db.session.delete(avenger)
    db.session.commit()
    response = avenger_schema.dump(avenger)
    return jsonify(response)