from calendar import c
from crypt import methods
from hashlib import new
from http.client import NETWORK_AUTHENTICATION_REQUIRED
from multiprocessing.connection import answer_challenge
from tkinter import N
from unicodedata import category

from models import Category
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def paginate_response(request,Model):
    page = request.args.get("page",1,type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    paginated_res = Model.query.all()[start:end]


    return [res.format() for res in paginated_res]



def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app,resources={r"/api/*":{"origin":"*"}})


    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/api/categories',methods=["GET"])
    def get_categories():
        categories_db = Category.query.all()
        if not categories_db:
            abort(404)
        categories = {}
        for category in categories_db:
            categories[f"{category.id}"] = category.type
        
        return jsonify({
            "categories": categories
        }),200


    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    
    @app.route('/api/questions',methods=["GET"])
    def get_questions():

        questions_db = paginate_response(request,Question)
        
        if not questions_db:
            abort(404)
  
        return jsonify({
            "questions": questions_db,
            "totalQuestions": Question.query.count(),
            "categories" :{category.id: category.type for category in Category.query.all()},
            "currentCategory":None
        }), 200

        


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/api/questions/<int:question_id>',methods=["DELETE"])
    def delete_question(question_id):
        question = Question.find_question_byId(question_id)
        if not question:
            abort(404)
        else:
            try:
                question.delete()
                return {"message":"question successfully deleted"},204
            except:
                db.session.rollback()
                abort(422)
            finally:
                db.session.close()

    """
    
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/api/questions',methods=["POST"])
    def create_question():
        request_body = request.get_json()

        question = request_body.get('question')
        answer = request_body.get('answer')
        difficulty = request_body.get('difficulty')
        category = request_body.get('category')
        
        new_question = Question(question, answer, difficulty, category)
        try:
            new_question.insert()
            return {
                "message":"success creating new question"
            }, 201
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
  

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/api/searchquestions',methods=["POST"])
    def search_questions():
        search_term = request.get_json().get('searchTerm')
       
        search_results = [result.format() for result  in Question.find_question_byName(search_term)]

        if not search_results:
            abort(404)


        return jsonify({
            "questions": search_results,
            "totalQuestions": len(search_results),
             "currentCategory":None
        }),200
   

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/api/categories/<int:category_id>/questions',methods=["GET"])
    def get_category_questions(category_id):
        
        category_questions =[question.format() for question in Question.query.filter(Question.category==category_id).all()]

        if not category_questions:
            abort(404)

        return jsonify({
            "questions": category_questions,
            "totalQuestions":len(category_questions),
            "currentCategory": Category.query.filter(Category.id==category_id).first().type
        }),200


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/api/quizzes',methods=["POST"])
    def play_quiz():
        previous_questions = request.get_json().get('previous_questions')
        quiz_category =request.get_json().get('quiz_category')

        if not previous_questions and not quiz_category:
            abort(400)

        category_questions =[question.format() for question in Question.query.filter(Question.category==quiz_category['id']).all()]


        while True:
            random_question = random.choice(category_questions)
            if random_question['id'] not in previous_questions:
                break
        
        return {
            "question":random_question
        },200


    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

