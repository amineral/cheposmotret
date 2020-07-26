from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    added_movies = db.relationship('Movie', backref='movies', lazy=True)


    def __repr__(self):
        return f'{self.username}'
    
    @classmethod
    def create_user(self, username, password):
        self.new_user = User(username=username, password=password)
        db.session.add(self.new_user)
        db.session.commit()
    
    @classmethod
    def add_movie(self, title, about, user):
        m = Movie(title=title, about=about)
        db.session.add(m)
        user.added_movies.append(m)
        db.session.commit()
        

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32), nullable=False)
    about = db.Column(db.String(100), nullable=True)
    added_by = db.Column(db.Integer, db.ForeignKey('user.username'))
    rate = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return f"{self.title}"
