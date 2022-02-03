"""Blogly application."""

from models import User, Post
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

### User Routes ###############################################################


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

    form_data = request.form
    first_name = form_data['first_name']
    last_name = form_data['last_name']
    image_url = form_data['image_url']

    User.create_new_user(first_name, last_name, image_url)
    db.session.commit()

    return redirect('/users')


@app.get('/users/<int:id>')
def show_selected_user_page(id):
    """Show the selected user page"""

    user = User.query.get_or_404(id)

    return render_template('user_page.html', user=user)


@app.get('/users/<int:id>/edit')
def show_edit_selected_user_form(id):
    """Show a form to edit the selected user."""

    user = User.query.get_or_404(id)

    return render_template('edit_user.html', user=user)


@app.post('/users/<int:id>/edit')
def update_user_record(id):
    """Save update to user record from user edit form."""

    user = User.query.get(id)

    form_data = request.form
    user.first_name = form_data['first_name']
    user.last_name = form_data['last_name']
    user.image_url = form_data['image_url']

    db.session.commit()

    return redirect(f'/users/{id}')

# cannot be a get request


@app.post('/users/<int:id>/delete')
def delete_user_record(id):
    """Delete the user record from the user page"""

    User.query.filter(User.id == id).delete()
    db.session.commit()

    return redirect('/users')

### Post Routes ###############################################################


@app.get('/users/<int:id>/posts/new')
def show_new_post_form(id):
    """Show the new post form for the specified user"""

    user = User.query.get(id)
    return render_template('new_post.html', user=user)


@app.post('/users/<int:id>/posts/new')
def create_post_and_redirect(id):
    """Create the post and redirect to the user detail page"""

    form_data = request.form

    title = form_data['title']
    content = form_data['content']
    user_id = id

    Post.create_new_post(title, content, user_id)
    db.session.commit()

    return redirect(f'/users/{id}')
