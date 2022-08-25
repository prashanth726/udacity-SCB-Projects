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
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_all_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_single_question(self):
        #insert a new question for testing
        question = Question(question='Who is the founder of Google', answer='Larry', category=6, difficulty=1)
        question.insert()
        res = self.client().delete('/questions/{question.id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_question(self):
        #random data for inserting new question
        question_data ={
            'question': 'Who is the founder of Google',
            'answer': 'Larry',
            'category': 6,
            'difficulty': 2
        }
        data = json.dumps(data)

        res = self.client().post('/api/questions', data=question_data, content_type='application/json')
        data = json.loads(req.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_with_random_question_id(self):
        #random question_id for deleting question
        random_question_id = 500000

        res = self.client().delete('/api/questions/{random_question_id}/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()