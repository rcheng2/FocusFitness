""" Python script to run tests """
import os
import unittest
from flask import current_app

os.environ[
    "DATABASE_URL"
] = "sqlite://"  # required to be here to use in-memory database for tests
os.environ["SECRET_KEY"] = "top_secret_key_lol"  # same as above
from app import app  # pylint: disable = wrong-import-position
from database import db  # pylint: disable = wrong-import-position


class TestWebApp(unittest.TestCase):
    """Tests for the web app"""

    def setUp(self):
        """Set up testing environment. Create sqlite db
        to test db in memory"""
        self.app = app
        self.app.config["WTF_CSRF_ENABLED"] = False
        self.appctx = self.app.app_context()
        self.appctx.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        """Clear testing environment."""
        db.drop_all()
        self.appctx.pop()
        self.app = None
        self.appctx = None
        self.client = None

    def test_app(self):
        """Check if testing environement is
        configured properly"""
        assert self.app is not None
        assert current_app == self.app

    def test_landing_page(self):
        """Tests if landing loads properly"""
        response = self.client.get("/")
        assert response.status_code == 200

    def test_signup_form(self):
        """Tests if signup form has correct components"""
        response = self.client.get("/signuppage")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'name="newuserid"' in html
        assert 'name="newpassword"' in html

    def test_login_form(self):
        """Tests if login form has correct components"""
        response = self.client.get("/login")
        assert response.status_code == 200
        html = response.get_data(as_text=True)

        assert 'name="userid"' in html
        assert 'name="pwd"' in html

    def test_register_and_login_new_user(self):
        """Test signing up new user and also logging them in"""
        # register new user below:
        response = self.client.post(
            "/registernewuser",
            data={"newuserid": "new_user", "newpassword": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert response.request.path == "/login"

        # login in new user
        response = self.client.post(
            "/loginuser",
            data={"userid": "new_user", "pwd": "password123"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        html = response.get_data(as_text=True)
        assert "Welcome new_user" in html


if __name__ == "__main__":
    unittest.main()
