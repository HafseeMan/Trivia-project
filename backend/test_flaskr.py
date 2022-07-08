import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        #Executed before each test
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        
        #setting up secrets from virtual environment
        self.database_user = os.getenv("DB_USER")
        self.database_password = os.getenv("DB_PASSWORD")
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.database_user, self.database_password, 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)


        # sample question for use in tests
        self.new_question = {
            "answer": "Repunzul", 
            "category": 4, 
            "difficulty": 2, 
            "question": "Which disney character has the longest hair?"
        }

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
    #---------- GET Categories ----------
    #  Success
    def test_get_categories(self):
        #condition
        res = self.client().get("/categories")
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["total_categories"])
    # Fail
    def test_error_404_get_categories(self):
        #condition
        res = self.client().patch('/categories/1')
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "Not found")
        self.assertEqual(data['success'], False)

    #---------- GET Questions (paginated) ----------
    #   Success
    def test_get_questions_paginated(self):
        #condtion
        res = self.client().get('/questions')
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    #   Fail
    def test_404_request_beyond_valid_page(self):
        #condition  
        res = self.client().get('/questions?page=90') #if out of range
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')
    
    #---------- DELETE Questions  ----------
    # Success
        
    def test_delete_question(self):
        #condtion
        res = self.client().delete("/questions/17")
        data = json.loads(res.data)
        #return question from database
        question = Question.query.filter(Question.id == 17).one_or_none()
        
        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 17)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))
        self.assertEqual(question, None)
    
    # Fail
    def test_422_if_question_does_not_exist(self):
        # Success
        res = self.client().delete("/questions/90")
        data = json.loads(res.data)
    
        # check status code and message
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")
    
    #---------- POST new Question  ----------
    # Success
    def test_create_new_question(self):
        #condition
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["question_created"])
        self.assertTrue(len(data["questions"]))
    
    # Fail
    def test_404_if_question_creation_not_valid(self):
        res = self.client().post("/books/45", json={"answer": "Repunzul"})
                                                    #incomplete fields
        data = json.loads(res.data)

        # check status code and message
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not found")    

    
    #---------- POST search Question  ----------
    # Success
    def test_search_questions(self):
        # send post request with search term
        res = self.client().post('/questions',
                                      json={'searchTerm': 'title'})
        # conditions
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

        # check if one of correct matches is included in response
        self.assertEqual(data['questions'][0]['id'], 5)
    
    # Fail
    def test_404_if_search_questions_fails(self):
        response = self.client().post('/questions',
                                      json={'searchTerm': ''})

        #condition
        data = json.loads(response.data)

        # check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not found')

    
    #---------- GET Questions (based on category) ----------
    #   Success   
    def test_get_questions_by_category(self):
        #condition
        res = self.client().get('/categories/2/questions') #for category id=2 
        data = json.loads(res.data)

        # response status code and message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertNotEqual(len(data['questions']), 0)
    
    # Fail
    def test_400_if_questions_by_category_fails(self):
        #condition
        res = self.client().get('/categories/10/questions') #Category out of range 1-6
        data = json.loads(res.data)

        # response status code and message
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()