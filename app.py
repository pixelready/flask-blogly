"""Blogly application."""

from models import User
from flask import Flask, redirect, render_template
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