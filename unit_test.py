from cgi import test
import unittest, requests
from app import calculate, app


class TestFlask(unittest.TestCase):
    def test_index(self):
        """ Test if current landing page (login page) is setup correctly"""
        tester = app.test_client(self)
        response = tester.get("/", content_type = 'html/text')
        self.assertEqual(response.status_code, 200)


# class TestCalculate(unittest.TestCase):
#     def test_calculate(self):
#         """ Unit test for calculate function """
#         resp = requests.post("http://172.17.110.195:8080/calculate", {"duration": 60,
#         "weight": 100, "exercise_type": "cardio"})
#         self.assertGreater(calculate, 1)

if __name__ == "__main__":
    unittest.main()