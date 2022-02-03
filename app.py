"""Blogly application."""

from models import User
from flask import Flask, redirect, render_template, request
from models import db, connect_db
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = 'jomamma'
toolbar = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

# make class method in users


def create_new_user(fname, lname, image):
    # fix indentation & docstring
    new_user = User(
        first_name=fname,
        last_name=lname,
        image_url=image)

    db.session.add(new_user)
    # this function should not commit. The route should make the commit
    db.session.commit()


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

    # change response to data or some other name
    response = request.form
    first_name = response.get('first_name')  # don't need the get, just use []
    last_name = response.get('last_name')
    image_url = response.get('image_url')

    create_new_user(first_name, last_name, image_url)
    return redirect('/users')


@app.get('/users/<int:id>')
def show_selected_user_page(id):
    """Show the selected user page"""

    user = User.query.get(id)

    return render_template('user_page.html', user=user)


@app.get('/users/<int:id>/edit')
def show_edit_selected_user_form(id):
    """Show a form to edit the selected user."""

    # get or 404 method to avoid having someone access an invalid id
    user = User.query.get(id)

    return render_template('edit_user.html', user=user)


@app.post('/users/<int:id>/edit')
def update_user_record(id):
    """Save update to user record from user edit form."""

    user = User.query.get(id)

    response = request.form
    user.first_name = response.get('first_name')
    user.last_name = response.get('last_name')
    user.image_url = response.get('image_url')

    db.session.commit()

    return redirect(f'/users/{id}')

# cannot be a get request


@app.get('/users/<int:id>/delete')
def delete_user_record(id):
    """Delete the user record from the user page"""

    User.query.filter(User.id == id).delete()
    db.session.commit()

    return redirect('/users')
