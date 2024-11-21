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
from models import db, User, People, Planets, Favorites
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

# get all users
@app.route('/users', methods=['GET'])
def show_users():

    users = User.query.all()
    serialized_users = [ user.serialize() for user in users ] 

    return jsonify(serialized_users), 200

# Get favorites per user
@app.route('/users/favorites', methods=['GET'])
def fav_per_user():
    favorites = Favorites.query.all()
    serialized_favorites = [ favorite.serialize() for favorite in favorites ]

    return jsonify(serialized_favorites), 200

# Get all People and Planets
@app.route('/people', methods=['GET'])
def show_people():

    people = People.query.all()
    serialized_people = [ person.serialize() for person in people ] 

    return jsonify(serialized_people), 200

@app.route('/planets', methods=['GET'])
def show_planets():

    planets = Planets.query.all()
    serialized_planets = [ planet.serialize() for planet in planets ] 

    return jsonify(serialized_planets), 200

@app.route('/favorites', methods=['GET'])
def show_favorites():

    favorites = Favorites.query.all()
    serialized_favorite = [ favorite.serialize() for favorite in favorites ] 

    return jsonify(serialized_favorite), 200


# Get individual people and planets
@app.route('/people:<int:id>', methods=['GET'])
def get_person(id):

    searched_person = People.query.get(id)
    
    if searched_person != None:
        return jsonify(searched_person.serialize()), 200
    
    return jsonify({"error": "Person doesn't exist"}), 400
    
@app.route('/planet:<int:id>', methods=['GET'])
def get_planet(id):

    searched_planet = Planets.query.get(id)
    
    if searched_planet != None:
        return jsonify(searched_planet.serialize()), 200
    
    return jsonify({"error": "Planet doesn't exist"}), 400

# add Favorites
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_planet(planet_id):
    body = request.json
    email = body.get("email")
    planet = Planets.query.get(planet_id)

    if planet == None:
        return jsonify({"error": "Planet doesn't exist"}), 404
    user = User.query.filter_by(email = email).one_or_none()
    if user == None:
        jsonify({"error": "User doesn't exist"}), 404

    new_favorite = Favorites()

    new_favorite.planet = planet

    new_favorite.user = user
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_people(people_id):
    body = request.json
    email = body.get("email")
    people = People.query.get(people_id)

    if people == None:
        return jsonify({"error": "person doesn't exist"}), 404
    user = User.query.filter_by(email = email).one_or_none()
    if user == None:
        jsonify({"error": "User doesn't exist"}), 404

    new_favorite = Favorites()

    new_favorite.people = people

    new_favorite.user = user
    db.session.add(new_favorite)
    db.session.commit()
    return jsonify(new_favorite.serialize()), 200

# delete Favorites

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_planet(planet_id):

    favorite_planet = Favorites.query.get(planet_id)
    
    if favorite_planet != None:
        db.session.delete(favorite_planet)
        db.session.commit()
        return jsonify(favorite_planet.serialize()), 200
    
    return jsonify({"error": "No esta en favoritos"})

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_person(people_id):

    favorite_person = Favorites.query.get(people_id)
    
    if favorite_person != None:
        db.session.delete(favorite_person)
        db.session.commit()
        return jsonify(favorite_person.serialize()), 200
    
    return jsonify({"error": "No esta en favoritos"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
