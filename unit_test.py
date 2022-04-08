import unittest, requests
from unittest.mock import MagicMock, patch
from flask import Flask
from app import calculate, app
from quotes import get_quote
from database import Record,db
from flask_testing import TestCase



class TestFlaskRoutes(unittest.TestCase):
    """ Unit tests for selected routes """

    def test_index_route(self):
        """ Test if current landing page (login page) is setup correctly
        by return status code 200 from a get request"""
        tester = app.test_client(self)
        response = tester.get("/", content_type = 'html/text')
        self.assertEqual(response.status_code, 200)


    def test_signup_route(self):
        """ Test if the /signuproute is setup correctly
        by return status code 200 from a get request"""
        tester = app.test_client(self)
        response = tester.get("/signuppage", content_type = 'html/text')
        self.assertEqual(response.status_code, 200)

    def test_index_unauthorized(self):
        """ Tests if login_required is working for the index route"""
        tester = app.test_client(self)
        response = tester.get('/index', content_type = "html/text")
        self.assertIsNot(response.status_code, 200)
    

class TestLoginAndSignUp(unittest.TestCase):
    """ Unit tests for the login and signup pages """

    def test_login_feature(self):
        """ Test to check if login function works """
        tester = app.test_client(self)
        response = tester.post('/loginuser', data = dict(userid = "arshad",
        pwd = "arshad"), follow_redirects = True
        )
        self.assertIn(b'Welcome', response.data)

    def test_login_feature_flash_msg(self):
        """ Test to check if flask throws error msg when credentials are 
        wrong """
        tester = app.test_client(self)
        response = tester.post('/loginuser', data = dict(userid = "qwerqwerqwer",
        pwd = "arshfdsdafasdfad"), follow_redirects = True)
        self.assertIn(b'User does not exist or you entered the wrong credentials. Try Again!',
        response.data)

    def test_sign_in_user_already_exists(self):
        """ Unit test for calculate function """
        tester = app.test_client(self)
        response = tester.post('/signuppage', data = dict(newuserid = "arshad",
        newpassword = "arshad"), follow_redirects = True)
        self.assertIn(b'Enter your new username below!', response.data)


class TestCalculate(unittest.TestCase):
    """ Unit tests for /calculate route """
    def test_calculate_cardio(self):
        """ Unit test for calculate function """
        tester = app.test_client(self)
        response = tester.post('/calculate', data = dict(duration = "60",
        weight = "100", exercise_type = "cardio"), follow_redirects = True
        )
        app.config['LOGIN_DISABLED'] = True
        self.assertIn(b'Calories burned: 735.0 kcal', response.data)

    def test_calculate_weightlifting(self):
        """ Unit test for calculate function """
        tester = app.test_client(self)
        response = tester.post('/calculate', data = dict(duration = "60",
        weight = "100", exercise_type = "weightlifting"), follow_redirects = True
        )
        app.config['LOGIN_DISABLED'] = True
        self.assertIn(b'Calories burned: 525.0 kcal', response.data)
        
    def test_calculate_swimming_or_other(self):
        """ Unit test for calculate function """
        tester = app.test_client(self)
        response = tester.post('/calculate', data = dict(duration = "60",
        weight = "100", exercise_type = "swimming"), follow_redirects = True
        )
        app.config['LOGIN_DISABLED'] = True
        self.assertIn(b'Calories burned: 315.0 kcal', response.data)


class QuotesTests(unittest.TestCase):
    """Unit test for quote function"""
    def test_get_quote(self):
        """mock response for quote"""
        mock_response = MagicMock()
        mock_response.json.return_value = {0: {"q": "random quote"}} 
        with patch("quotes.requests.get") as mock_requests_get:
            mock_requests_get.return_value = mock_response
            self.assertEqual(get_quote(), "random quote")
        
if __name__ == "__main__":
    unittest.main()