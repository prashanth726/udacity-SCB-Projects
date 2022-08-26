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
        
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            self.DB_USER, self.DB_PASSWORD, self.DB_HOST, self.DB_NAME)
        setup_db(self.app, self.DB_PATH)

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

        res = self.client().delete(f'/questions/{question.id}')
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
        data = json.dumps(question_data)
        
        res = self.client().post('/questions', json=question_data, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_question_failure(self):
        #random question_id for deleting question
        random_question_id = 500000

        res = self.client().delete(f'/questions/{random_question_id}/delete')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_create_new_question_failure(self):
        #random data for inserting new question
        question_data ={}
        data = json.dumps(question_data)

        res = self.client().post('/questions', json=question_data, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_search_questions_success(self):
        question = Question(question='Where are you ', answer='Who', category=6, difficulty=1)
        question.insert()
        search_data ={'searchTerm':'Where'}
        res = self.client().post('/questions/search', json=search_data, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_search_questions_failure(self):
        search_data ={}
        res = self.client().post('/questions', json=search_data, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_retrieve_questions_based_on_category_success(self):
        category_id = 1

        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)

    def test_retrieve_questions_based_on_category_failure(self):
        category_id = 10000

        res = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_play_quiz_success(self):
        quiz_data = {
            'previous_questions': [1],
            'quiz_category': {'id': 1, 'type': 'Sports'}
        }
        res = self.client().post('/quizzes', json=quiz_data, content_type='application/json')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_play_quiz_failure(self):
        quiz_data = {
           
        }
        res = self.client().post('/quizzes', json=quiz_data, content_type='application/json')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()