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

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    climate = db.Column(db.String(10), nullable=False)
    diameter = db.Column(db.String(10), nullable=False)
    gravity = db.Column(db.String(10), nullable=False)
    orbital_period = db.Column(db.String(10), nullable=False)
    population = db.Column(db.String(10), nullable=False)
    rotation_period = db.Column(db.String(10), nullable=False)
    surface_water = db.Column(db.String(10), nullable=False)
    terrain = db.Column(db.String(10), nullable=False)


 
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

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