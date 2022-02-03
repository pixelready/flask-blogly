"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
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

    def get_full_name(self):
        """return the full name as a string"""

        return f'{self.first_name} {self.last_name}'


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(150), nullable=False)
    post_content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    author = db.relationship('User', backref='posts')

    @classmethod
    def create_new_post(cls, title, post_content, user_id):
        """Create a new post and add to current transaction"""

        new_post = Post(title=title, post_content=post_content,
                        user_id=user_id)

        db.session.add(new_post)
