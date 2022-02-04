from unittest import TestCase

from app import app, db
from models import User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()
        

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            image_url=None)

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            image_url=None
        )

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

        test_user_post1 = Post(
            title="test_first_post",
            post_content="content goes here",
            user_id=self.user_id
        )

        test_user_post2 = Post(
            title="test_second_post",
            post_content="content goes here 2",
            user_id=self.user_id
        )

        db.session.add_all([test_user_post1, test_user_post2])
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Does the user list show the test user?"""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_new_user_form_displays(self):
        """Does the new user form display from the new user route?"""
        with self.client as c:
            resp = c.get("/users/new")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn('action="/users/new"', html)

    def test_new_user_creation(self):
        """Does the new user creation route create the user in the db?"""

        first_name = 'disguy'
        last_name = 'ovahhere'
        image_url = 'https://2.bp.blogspot.com/-L-0e2jsHy1I/T1Wmt52vCDI/AAAAAAAAC2A/i5fncCyOFSE/s400/dicktracyflattop.jpg'

        with self.client as c:
            post = c.post(
                '/users/new',
                data={
                    'first_name': first_name,
                    'last_name': last_name,
                    'image_url': image_url}
            )

            self.assertEquals(post.status_code, 302)

        user = User.query.filter(User.first_name == 'disguy').first()

        self.assertIsNotNone(user)

    def test_user_detail_page_display(self):
        """Does the user detail page get displayed?"""

        with self.client as c:
            resp = c.get(f"users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertIn('test_last</h1>', html)

    def test_edit_form_filled(self):
        """Does the edit page come pre-populated with the user server data?"""

        with self.client as c:
            resp = c.get(f"users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertIn('value="test_first"', html)
            self.assertIn('value="test_last"', html)
            self.assertIn('value="None"', html)

    ###### Post Tests ##################################################

    def test_new_post_form_display(self):
        """Does the new form page display correctly?"""

        with self.client as c:
            resp = c.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertIn("Testing for create post page", html)

    def test_new_post_creation(self):
        """Does the new post form create a new post in the db?"""

        with self.client as c:
            # breakpoint()
            c.post(
                f"/users/{self.user_id}/post/new",
                data={'title': 'abcdef*', 'post_content': 'contentxy'}
            )
            
            post = Post.query.filter(Post.title == 'abcdef*')
            self.assertIsNotNone(post)
