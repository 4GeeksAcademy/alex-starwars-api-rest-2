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
from models import db, User, Character, Planet, Favorite
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

@app.route('/users', methods=['GET'])
def handle_users():
    users = db.session.query(User).all() 
    users_list = [user.serialize() for user in users]

    return jsonify(users_list), 200

@app.route('/people', methods=['GET'])
def handle_people():
    characters = db.session.query(Character).all()

    if characters:
        characters_list = [char.serialize() for char in characters]
        return jsonify(characters_list), 200
    else:
        return 'There is no character here, add one and try again!', 404
    
@app.route('/people/<int:people_id>', methods=['GET'])
def handle_specific_people(people_id):
    character = db.session.query(Character).filter_by(id=people_id).first()
    if character:
        character = character.serialize()
        return jsonify(character), 200
    else:
        return "there is no character with this id", 404

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = db.session.query(Planet).all()
    if planets:
        planets_list = [planet.serialize() for planet in planets]
        return jsonify(planets_list), 200
    else:
        return ' There is no planet here, add one and try again'

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_specific_planet(planet_id):
    planet= db.session.query(Planet).filter_by(id=planet_id).first()
    if planet:
        return jsonify(planet.serialize()), 200
    else:
        return 'There is no planet with that id, try again', 404

@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def handle_favorite_planet(planet_id):
    data = request.get_json()
    user_id_from_body = data.get("user_id")

    user_from_database = db.session.query(User).filter_by(id=user_id_from_body).first()
    planet_from_database = db.session.query(Planet).filter_by(id=planet_id).first()
    new_favorite = Favorite(user_id = user_from_database.id, planet_id= planet_from_database.id, character_id=1)

    db.session.add(new_favorite)
    db.session.commit()

    return "Favorite added successfully", 201

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def handle_delete_favorite_planet(planet_id):
    favorite_to_delete = db.session.query(Favorite).filter_by(planet_id = planet_id).first()

    db.session.delete(favorite_to_delete)
    db.session.commit()
    
    return "Favorite deleted successfully", 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def handle_favorite_people(people_id):
    data = request.get_json()
    user_id_from_body = data.get("user_id")

    user_from_database = db.session.query(User).filter_by(id=user_id_from_body).first()
    people_from_database = db.session.query(Character).filter_by(id=people_id).first()
    new_favorite = Favorite(user_id = user_from_database.id, planet_id= 1, character_id=people_from_database.id)

    db.session.add(new_favorite)
    db.session.commit()
    
    return "Favorite added successfully", 201
    # favorites = db.session.query(Favorite).all()
    # favorites_list = [fav.serialize() for fav in favorites]
    # return favorites_list, 201

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def handle_delete_favorite_people(people_id):
    favorite_to_delete = db.session.query(Favorite).filter_by(character_id = people_id).first()

    db.session.delete(favorite_to_delete)
    db.session.commit()
    
    return "Favorite deleted successfully", 200
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

