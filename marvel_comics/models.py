from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import uuid

from werkzeug.security import generate_password_hash
import secrets

from datetime import datetime
from flask_login import UserMixin, LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
ma = Marshmallow()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key = True)
    first_name = db.Column(db.String(150), nullable = True, default = '')
    last_name = db.Column(db.String(150), nullable = True, default = '')
    email = db.Column(db.String(150), nullable = False)
    password = db.Column(db.String, nullable = True, default = '')
    g_auth_verify = db.Column(db.Boolean, default = False)
    token = db.Column(db.String, default = '', unique = True)
    date_created = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    avenger = db.relationship('Avenger', backref='owner', lazy = True)

    def __init__(self, email, first_name = '', last_name = '', id = '', password = '', token = '', g_auth_verify = False):
        self.id = self.set_id()
        self.first_name = first_name
        self.last_name = last_name
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify


    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database!'

class Avenger(db.Model):
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String(150))
    power_abilities = db.Column(db.String())
    height = db.Column(db.Numeric(precision = 4, scale = 2))
    movies = db.Column(db.String())
    comics = db.Column(db.String())
    allies = db.Column(db.String())
    enemies = db.Column(db.String())
    groups = db.Column(db.String(250))
    living_or_decease = db.Column(db.String(100))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False)

    def __init__(self, name, power_abilities, height, movies, comics, allies, enemies, groups, 
    living_or_decease, user_token, id = ''):
        self.id = self.set_id()
        self.name = name
        self.power_abilities = power_abilities
        self.height = height
        self.movies = movies
        self.comics = comics
        self.allies = allies
        self.enemies = enemies
        self.groups = groups
        self.living_or_decease = living_or_decease
        self.user_token = user_token

    def __repr__(self):
        return f'The following Avenger has been added: {self.name}'

    def set_id(self):
        return secrets.token_urlsafe()

class AvengerSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'power_abilities', 'height', 'movies', 'comics', 'allies', 
        'enemies', 'groups', 'living_or_decease']

avenger_schema = AvengerSchema()
avengers_schema = AvengerSchema(many = True)