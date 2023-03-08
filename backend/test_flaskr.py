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
        
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format('student','student','localhost:5432', self.database_name)
        self.app = create_app(self.database_path)
        self.client = self.app.test_client
   
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        # This test tests for the correct transmission of all categories
        res = self.client().get("/categories")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content["categories"].keys()), 1)
        self.assertEqual(content["success"], True)
    
    # TODO (possibly): catch wrong methods for endpoint categories

    def test_get_questions(self):
        res = self.client().get("/questions?page=1")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content["categories"].keys()), 1)
        self.assertEqual(len(content["questions"]), 10)
        self.assertEqual(content["success"], True)

    def test_get_questions_fail(self):
        res = self.client().get("/questions?page=1000000000")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(content["success"], False)
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()