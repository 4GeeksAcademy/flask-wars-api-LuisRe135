from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }


class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    birth_year = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.String(120), unique=True, nullable=False)
    hair_color = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<People %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "hair_color": self.hair_color,
            "height": self.height,
            "birth_year": self.birth_year
            
        }
    
class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.String(120), unique=True, nullable=False)
    orbital_period = db.Column(db.String(120), unique=True, nullable=False)
    gravity = db.Column(db.String(120), unique=True, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "gravity": self.gravity,
            "orbital_period": self.orbital_period,
            "population": self.population
            
        }
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable = True)
    planet = db.relationship(Planets)
    character_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable = True)
    character = db.relationship(People)

    def serialize(self):
        return {
            "id": self.id,
            "planet": self.planet.serialize() if self.planet != None else "",
            "character": self.character.serialize() if self.character != None else "",
            "user": self.user.serialize() if self.user != None else ""
        }