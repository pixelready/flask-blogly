"""Blogly application."""

from models import User
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.get('/')
def direct_to_users():
    """Directs to the /users page"""

    return redirect('/users')


@app.get('/users')
def show_all_users():
    """shows all the users"""

    users = User.get_users()

    return render_template("users.html", users=users)


@app.get('/users/new')
def show_create_user_form():
    """Show the Create new user form."""

    return render_template("new_user.html")


@app.post('/users/new')
def add_user_and_display_user_list():
    """Add a user and return to the /users page."""

    response = request.form
    first_name = response.get('first_name')
    last_name = response.get('last_name')
    image_url = response.get('image_url')

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        image_url=image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:id>')
def show_selected_user_page(id):
    """Show the selected user page"""

    user = User.query.get(id)

    return render_template('user_page.html', user=user)
