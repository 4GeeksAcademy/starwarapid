"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    return jsonify([person.to_dict() for person in people])

@app.route('/people', methods=['POST'])
def post_people():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    id = data.get('id')
    name = data.get('name')
    birth_year = data.get('birth_year')
    eye_color = data.get('eye_color')
    gender = data.get('gender')
    hair_color = data.get('hair_color')
    height = data.get('height')
    mass = data.get('mass')
    skin_color = data.get('skin_color')

    if not all([id, name, birth_year, eye_color, gender, hair_color, height, mass, skin_color]):
        return jsonify({'error': 'Missing required fields'}), 400

    new_person = People(
        id=id,
        name=name,
        birth_year=birth_year,
        eye_color=eye_color,
        gender=gender,
        hair_color=hair_color,
        height=height,
        mass=mass,
        skin_color=skin_color
    )
    db.session.add(new_person)
    db.session.commit()
    return jsonify(new_person.to_dict()), 201

@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({'error': 'Person not found'}), 404
    return jsonify(person.to_dict())

@app.route('/people/<int:people_id>', methods=['POST'])
def update_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({'error': 'Person not found'}), 404
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    for key, value in data.items():
        setattr(person, key, value)
    db.session.commit()
    return jsonify(person.to_dict()), 200

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({'error': 'Person not found'}), 404
    db.session.delete(person)
    db.session.commit()
    return jsonify({'message': 'Person deleted successfully'}), 200

@app.route('/planet', methods=['GET', 'POST'])
def handle_planets():
    if request.method == 'GET':
        planets = Planet.query.all()
        return jsonify([planet.to_dict() for planet in planets])
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        id = data.get('id')
        name = data.get('name')
        diameter = data.get('diameter')
        climate = data.get('climate')
        terrain = data.get('terrain')

        if not all([id, name, diameter, climate, terrain]):
            return jsonify({'error': 'Missing required fields'}), 400

        new_planet = Planet(
            id=id,
            name=name,
            diameter=diameter,
            climate=climate,
            terrain=terrain
        )
        db.session.add(new_planet)
        db.session.commit()
        return jsonify(new_planet.to_dict()), 201

@app.route('/planet/<int:planet_id>', methods=['GET', 'POST', 'DELETE'])
def handle_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({'error': 'Planet not found'}), 404

    if request.method == 'GET':
        return jsonify(planet.to_dict())
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        for key, value in data.items():
            setattr(planet, key, value)
        db.session.commit()
        return jsonify(planet.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(planet)
        db.session.commit()
        return jsonify({'message': 'Planet deleted successfully'}), 200

@app.route('/users', methods=['GET', 'POST'])
def handle_users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.to_dict() for user in users])
    elif request.method == 'POST':
        data = request.get_json()
        new_user = User(**data)
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.to_dict()), 201

@app.route('/users/<int:user_id>', methods=['GET', 'POST', 'DELETE'])
def handle_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        return jsonify({'error': 'User not found'}), 404

    if request.method == 'GET':
        return jsonify(user.to_dict())
    elif request.method == 'POST':
        data = request.get_json()
        for key, value in data.items():
            setattr(user, key, value)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200

@app.route('/users/favorites', methods=['GET', 'POST'])
def handle_user_favorites():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        if user_id is None:
            return jsonify({'error': 'User ID is required'}), 400
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        favorites = Favorite.query.filter_by(user_id=user_id).all()
        return jsonify([favorite.to_dict() for favorite in favorites])
    elif request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        if user_id is None:
            return jsonify({'error': 'User ID is required'}), 400
        user = User.query.get(user_id)
        if user is None:
            return jsonify({'error': 'User not found'}), 404
        favorite = Favorite(user_id=user_id, **data)
        db.session.add(favorite)
        db.session.commit()
        return jsonify(favorite.to_dict()), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
