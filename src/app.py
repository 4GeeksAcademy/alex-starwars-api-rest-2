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
        return 'There is no character here, add one and try again!'
    
@app.route('/people/<int:people_id>', methods=['GET'])
def handle_specific_people(people_id):
    character = db.session.query(Character).filter_by(id=people_id).first()
    if character:
        return jsonify(character.serialize())
    else:
        return "there is no character with this id"

@app.route('/planets', methods=['GET'])
def handle_planets():
    planets = db.session.query(Planet).all()
    if planets:
        planets_list = [planet.serialize() for planet in planets]
        return jsonify(planets_list)
    else:
        return ' There is no planet here, add one and try again'

@app.route('/planets/<int:planet_id>', methods=['GET'])
def handle_specific_planet():
    return 'specific planet'

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
