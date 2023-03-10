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
        # This test checks if the questions can be fetched successfully
        res = self.client().get("/questions?page=1")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content["categories"].keys()), 1)
        self.assertEqual(len(content["questions"]), 10)
        self.assertEqual(content["success"], True)

    def test_get_questions_fail(self):
        # This test checks if a error response is transmitted if a not-existing page is called for questions
        res = self.client().get("/questions?page=1000000000")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(content["success"], False)

    def test_post_question(self):
        # This test checks if posting a question with content works successfully
        res = self.client().post("/questions", json={
            "question": "TestQuestion",
            "answer": "TestAnswer",
            "difficulty": 1,
            "category": 1
        })
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(content["success"], True)
        self.assertIsNotNone(content["id"])
        self.assertIsNotNone(content["question"])

    def test_post_question_fail(self):
        # This test checks if posting a question erroneously (without content) is being caught
        res = self.client().post("/questions", json={
            "question": None,
            "answer": None,
            "difficulty": 1,
            "category": 1
        })
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(content["success"], False)

    def test_deletion(self):
        # This test checks, if deleting an existing question works correctly
        res = self.client().delete("/questions/23")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(content["success"], True)
        self.assertEqual(content["id"], 23)

    def test_deletion_fail(self):
        # This test checks, if deleting a non-existing question raises the right error
        res = self.client().delete("/questions/1000000")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(content["success"], False)

    def test_search_question(self):
        res = self.client().post("/questions", json={"searchTerm": "What"})
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(content["questions"]), 1)
        self.assertGreaterEqual(content["total_questions"], 1)
        self.assertEqual(content["success"], True)

    def test_search_question_fail(self):
        res = self.client().post("/questions")
        content = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(content["success"], False)

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()