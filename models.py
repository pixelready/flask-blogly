"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import null
import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    image_url = db.Column(db.String)

    @classmethod
    def get_users(cls):
        return User.query.all()

    @classmethod
    def create_new_user(cls, fname, lname, image):
        """Create a new user and add to current transaction"""
        new_user = User(
            first_name=fname,
            last_name=lname,
            image_url=image)

        db.session.add(new_user)


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.column(db.ForeignKey('users.id'))

    @classmethod
    def create_new_post(cls, title, content, user_id):
        """Create a new post and add to current transaction"""

        new_post = Post(title=title, content=content, user_id=user_id)

        db.session.add(new_post)
