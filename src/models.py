from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    birth_year = db.Column(db.String(10), nullable=False)
    eye_color = db.Column(db.String(10), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    hair_color = db.Column(db.String(10), nullable=False)
    height = db.Column(db.String(10), nullable=False)
    mass = db.Column(db.String(10), nullable=False)
    skin_color = db.Column(db.String(10), nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "birth_year": self.birth_year,
            "eye_color": self.eye_color,
            "gender": self.gender,
            "hair_color": self.hair_color,
            "height": self.height,
            "mass": self.mass,
            "skin_color": self.skin_color
        }

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(10), nullable=False)
    diameter = db.Column(db.String(10), nullable=False)
    terrain = db.Column(db.String(10), nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "diameter": self.diameter,
            "climate": self.climate,
            "terrain": self.terrain
        }


 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,

        }

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    planet_id = db.Column(db.Integer, db.ForeignKey('planet.id'), nullable=False)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }