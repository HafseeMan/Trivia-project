from distutils.log import debug
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#Helper method
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    #NB: Access-control-.. allows a domain to access an API database
    CORS(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    #CORS Headers
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/')
    def main():
        return jsonify({"message": "Welcome to my hooooood"})


    @app.route('/categories')
    @cross_origin()
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.format() for category in categories]

        return jsonify({
            'success':True,
            'categories': formatted_categories           
            })

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

    @app.route('/categories/questions')
    @cross_origin()
    def get_all_questions():
        ##PAGINATION
          #To display the first page by default if not specified in url
        page = request.args.get('page', 1, type=int)
          #Calculating position of (10) questions to be displayed based on page number
        start = (page-1) * QUESTIONS_PER_PAGE 
        end = start + QUESTIONS_PER_PAGE

        questions = Question.query.all()
        formatted_questions = [question.format() for question in questions]                

        return jsonify({
            'success':True,
            'categories': formatted_questions[start:end],
            'total_questions': len(formatted_questions)           
            })
 
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    @cross_origin()
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None:
               abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            remaining_questions = paginate_questions(request, selection)
            
            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": remaining_questions,
                "total_books": len(Question.query.all())
            })
            
        except:
            abort(422)
    
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"]) 
    @cross_origin()
    def create_question():
       #Get body from request
       body = request.get_json()

       new_question = body.get("question", None)
       new_answer = body.get("answer", None)
       new_category = body.get("category", None)
       new_difficulty = body.get("difficulty", None)

       try:

        #Creating book out of new parameters
        new_question = Question(question=new_question, answer=new_answer, category=new_category, difficulty=new_difficulty)
        #Adding to database
        new_question.insert()

        selection = Question.query.order_by(Question.id).all()
        newset_questions = paginate_questions(request, selection)
        
        return jsonify(
                {
                    "success": True,
                    "created": new_question.id,
                    "books": newset_questions,
                    "total_books": len(Question.query.all()),
                }
            )

       except:
          abort(422)




    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions/search", methods=["POST"])
    @cross_origin()
    def search_question():

        body = request.get_json()
        search = body.get('search', None)

        if search:
            selection = Question.query.filter(f'%{search}%').all()
        
        search_results = paginate_questions(request, selection)
        
        return jsonify({
                "success": True,
                "questions": search_results,
                "found_matches": len(selection.all())
            })

 

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    @cross_origin()
    def get_questions(category_id):

        #Filtering questions under category
        questions = Question.query.filter(Question.category==category_id)

        formatted_questions = [question.format() for question in questions]                

        #If category not existing
        if category_id not in [1,2,3,4,5,6]:
            abort(404)
        else:
            return jsonify({
                'success':True,
                'categories': formatted_questions,
                'total_questions': len(formatted_questions),
                })

  
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

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
   #Error messages to be sent as json to user instead of html page
    @app.errorhandler(400)#client error
    def bad_request(error):
        return jsonify({
            "success": False,
            "error":400,
            "message":"bad request"
        }), 400
  
    @app.errorhandler(404)
    def not_found(error): #page not found
        return jsonify({
            "success": False,
            "error":404,
            "message":"Not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error): #client request syntax not correct
        return jsonify({
            "success": False,
            "error":422,
            "message":"unprocessable"
        }), 422

    @app.errorhandler(500)
    def unexpected(error): 
        return jsonify({
            "success": False,
            "error":500,
            "message":"Unexpected condition"
        }), 500

    if __name__ == '__main__':
        app.run(debug=True)

    return app
