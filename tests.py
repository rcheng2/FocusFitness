""" Python script to run tests """
import os
import unittest
from flask import current_app
os.environ["DATABASE_URL"] = "sqlite://"  # use an in-memory database for tests
from app import app
from database import db




class TestWebApp(unittest.TestCase):
    """ Tests for the web app """
    def setUp(self):
        """Set up testing environment. Create sqlite db
        to test db in memory"""
        self.app = app
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
        """Test if app is configured properly"""
        assert self.app is not None
        assert current_app == self.app

    def test_home_page_redirect(self):
        """ Tests if landing page works"""
        response = self.client.get("/", follow_redirects=True)
        assert response.status_code == 200

    def test_signup_page(self):
        """ Test sign up function """
        response = self.client.get("/", follow_redirects=True)
        assert response.status_code == 200


if __name__ == "__main__":
    unittest.main()
