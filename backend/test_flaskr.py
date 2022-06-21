
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy


from flaskr import create_app
from models import setup_db, Question, Category
from settings import TEST_DB_NAME,DB_USER


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = TEST_DB_NAME
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
    def test_get_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(data["categories"])
    
    def test_404_get_categories(self):
        res = self.client().get('/api/categorie')
        data =json.loads(res.data)
        self.assertEqual(res.status_code,404)
        self.assertEqual(data["message"],"resource not found")
        self.assertEqual(data["status"],"fail")
    
    def test_get_questions(self):
            res = self.client().get('/api/questions?page=1')
            data = json.loads(res.data)

            self.assertEquals(res.status_code, 200)
            self.assertTrue(data["total_questions"])
            self.assertTrue(data["questions"])
            self.assertTrue(data["categories"])
            self.assertEqual(data["current_category"],'History')
    
    def test_404_get_questions(self):
            res = self.client().get('/api/questions?page=10000')
            data = json.loads(res.data)

            self.assertEqual(res.status_code,404)
            self.assertEqual(data["message"],"resource not found")
            self.assertEqual(data["status"],"fail")
    
   
    
        
    def test_404_delete_questions(self):
            res = self.client().delete('/api/questions/10000')
            data = json.loads(res.data)

            self.assertEqual(res.status_code,404)
            self.assertEqual(data["message"],"resource not found")
            self.assertEqual(data["status"],"fail")

    def test_create_question(self):
        res = self.client().post('/api/questions',json={
        "question":"what is your name",
        "answer":"chidera",
        "difficulty":1,
        "category":2
        })

        data = json.loads(res.data)
        self.assertEqual(res.status_code,201)
        self.assertEqual(data["message"],"success creating new question")
    
    def test_400_create_question(self):
        res = self.client().post('/api/questions',json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data["message"],"Invalid request body")
        self.assertEqual(data["status"],"fail")
    
    def test_Search_question(self):
        res = self.client().post('/api/searchquestions',json={
        "searchTerm": "name"
        })
        data = json.loads(res.data)

        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(data['total_questions'])
        self.assertEqual(data["current_category"],None)
    
    def test_400_Search_question(self):
        res = self.client().post('/api/searchquestions',json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data["message"],"Invalid request body")
        self.assertEqual(data["status"],"fail")
            
    def test_404_Search_questions(self):
            res = self.client().post('/api/searchquestions',json={
            "searchTerm":"polog"
            })
            data = json.loads(res.data)

            self.assertEqual(res.status_code,404)
            self.assertEqual(data["message"],"resource not found")
            self.assertEqual(data["status"],"fail")

    def test_get_by_category (self):
        res = self.client().get('/api/categories/5/questions')
        data= json.loads(res.data)

        self.assertEquals(res.status_code, 200)
        self.assertTrue(len(data["questions"])>0)
        self.assertTrue(data["current_category"],data["questions"][0]["category"])
        self.assertTrue(data["total_questions"])
    
    def test_404_get_by_category(self):
        res = self.client().get('/api/categories/1000/questions')
        data= json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data["message"],"resource not found")
        self.assertEqual(data["status"],"fail")

    def test_quizzes(self):
        sample_quiz ={
    "previous_questions": [1, 4, 20],
    "quiz_category":{"id":1,"type":"Science"}
 }
        res = self.client().post('/api/quizzes',json=sample_quiz)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question']['id'] not in sample_quiz['previous_questions'])
        self.assertTrue(data['question'])



    def test_400_quizzes(self):
        res = self.client().post('/api/quizzes')
        data = json.loads(res.data)

        self.assertEqual(res.status_code,400)
        self.assertEqual(data["message"],"Invalid request body")
        self.assertEqual(data["status"],"fail")

    def test_404_nonexistingtoutes(self):
        res = self.client().get('/*')
        data= json.loads(res.data)

        self.assertEqual(res.status_code,404)
        self.assertEqual(data["message"],"resource not found")
        self.assertEqual(data["status"],"fail")





    


    
            



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()