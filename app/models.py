from app import db,login,app
from datetime import datetime
from flask_login import UserMixin
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
class User(UserMixin,db.Model):
        __tablename__ = 'users'
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))
        about_me = db.Column(db.String(140))
        def __repr__(self):
             return '<User {}>'.format(self.username)
        def set_password(self,password):
            self.password_hash = generate_password_hash(password)
        def check_password(self, password):
            return check_password_hash(self.password_hash, password)
        def avatar(self,size):
            digest = md5(self.email.lower().encode('utf-8')).hexdigest()
            return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class movie_details(UserMixin,db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    lang = db.Column(db.String(), nullable=False)
    mtype = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), nullable=False)
    rating = db.Column(db.Float())
    desc = db.Column(db.String())
    def __repr__(self):
        return '<movie_details {}>'.format(self.name)

class Reviews(db.Model):
        __tablename__ ='review'

        id = db.Column(db.Integer, primary_key=True)
        comment = db.Column(db.String())
        rate = db.Column(db.Float())
        timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
        movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
        def __repr__(self):  
             return '<Reviews {}>'.format(self.comment)


@login.user_loader
def load_user(id):
        return User.query.get(int(id))
@app.shell_context_processor
def make_shell_context():
    return {'db':db,'User':User}


