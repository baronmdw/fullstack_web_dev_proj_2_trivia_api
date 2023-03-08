import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # TODO: make sure to initiate the correct database, see: https://stackoverflow.com/questions/75523569/runtimeerror-a-sqlalchemy-instance-has-already-been-registered-on-this-flask
        
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student','student','localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
   
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_Hello(self):
        res = self.client().get("/")

        self.assertEqual(res.json['cats'][6], "Hello World")
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()