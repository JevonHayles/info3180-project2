from . import db
from werkzeug.security import generate_password_hash
from datetime import datetime

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(200))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(200))
    biography = db.Column(db.String(500))
    profile_photo = db.Column(db.String(200))
    joined_on = db.Column(db.DateTime, default=datetime.now)   

    def __init__(self, username, password, first_name, last_name, email, location, biography, profile_photo, joined_on):
        self.username = username
        self.password = generate_password_hash(password, method='pbkdf2:sha256')
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.biography = biography
        self.profile_photo = profile_photo
        self.joined_on = joined_on

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support

    def __repr__(self):
        return '<User %r>' % (self.username)
    
class FollowTB(db.Model):
    __tablename__ = 'follow_tb'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, follower_id, user_id):
        self.follower_id = follower_id
        self.user_id = user_id

class LikesTB(db.Model):
    __tablename__ = 'likes_tb'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer)

    def __init__(self, post_id, user_id):
        self.post_id = post_id
        self.user_id = user_id

class PostsTB(db.Model):
    __tablename__ = 'posts_tb'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(200))
    photo = db.Column(db.String(200))
    user_id = db.Column(db.Integer)
    created_on = db.Column(db.DateTime, default=datetime.now)   

    def __init__(self, caption, photo, user_id, created_on):
        self.caption = caption
        self.photo = photo
        self.user_id = user_id
        self.created_on = created_on