from curses import raw
from distutils.log import debug
import json
import os
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random
from matplotlib.style import available

from sqlalchemy import false

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
    
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        #CORS Headers
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    @cross_origin()
    def get_categories():
        #retrieve categories from database
        categories = Category.query.all()
        #Changing formatting from {"id":1, "type":"science"} to {1:"science"}  
        # as expected by frontend
        formatted_categories = {category.id:category.type for category in categories}

        # abort 404 if no categories found
        if (len(formatted_categories) == 0 or not categories or categories == None):
            abort(404)

        return jsonify({
            'success':True,
            'categories': formatted_categories,           
            'total_categories': len(categories)
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

    @app.route('/questions')
    @cross_origin()
    def get_all_questions():
        #Retrieving questions in database
        selection = Question.query.all()
        # paginate the results
        paginated = paginate_questions(request, selection)

        #Error if no questions found
        if len(paginated) == 0:
            abort(404)

        # get all categories from database and adding dictionary
        categories = Category.query.all()
        categories_dict = {}

        for category in categories:
            categories_dict[category.id] = category.type


        return jsonify({
            'success':True,
            'categories': {category.id:category.type for category in categories},           
            'total_questions': len(paginated),           
            'questions': paginated,
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
            #Finding targeted question object in database
            question = Question.query.filter(Question.id == question_id).one_or_none()
            
            if question is None:
               abort(422)

            question.delete()
            selection = Question.query.all()
            remaining_questions = paginate_questions(request, selection)
            
            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": remaining_questions,
                "total_questions": len(Question.query.all())
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

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.route("/questions", methods=["POST"]) 
    @cross_origin()
    def create_or_search_question():
        '''
        Handles POST requests for creating new questions and searching questions.
        '''
        # load the request body
        body = request.get_json()

        # if search term is present
        if (body.get('searchTerm')):
            search_term = body.get('searchTerm')

            # 404 if search body empty
            if search_term is None:
                abort(404)

            selection = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()

            # paginate the results
            paginated = paginate_questions(request, selection)
        
            return jsonify({
                'success': True,
                'questions': paginated,
                'total_questions': len(Question.query.all())
            })
        # if no search term, create new question
        else:
            # load data from body
            new_question = body.get('question')
            new_answer = body.get('answer')
            new_difficulty = body.get('difficulty')
            new_category = body.get('category')

            # ensure all fields have data
            if ((new_question is None) or (new_answer is None)
                    or (new_difficulty is None) or (new_category is None)):
                abort(404)

            try:
                # create and insert new question
                question = Question(question=new_question, answer=new_answer,
                                    difficulty=new_difficulty, category=new_category)
                question.insert()

                # get all questions and paginate
                selection = Question.query.order_by(Question.id).all()
                current_questions = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'created': question.id,
                    'question_created': question.question,
                    'questions': current_questions,
                    'total_questions': len(Question.query.all())
                })

            except:
                # abort unprocessable if error
                abort(422)



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

        # get all categories and add to array
        categories = Category.query.all()
        categories_arr = {}

        for category in categories:
            categories_arr[category.id] = category.type        

        #If category not existing
        if category_id not in categories_arr:
            abort(400)
        else:
            return jsonify({
                'success':True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'categories': categories_arr,
                'current_category':  category_id
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
    @app.route('/quizzes', methods=['POST'])
    @cross_origin()
    def play_quiz():
        # load the request body
        body = request.get_json()
        # get the previous questions and category
        previous_questions = body.get('previous_questions')
        category = body.get('quiz_category')

        try:
            # -- load questions
            # if category specified 
            if (category and category['id'] != 0):
                #Filter out questions not included in previous_questions array
                questions_raw = (Question.query
                .filter(Question.category == str(category['id']))
                .all())
            #if category not specified
            else:
                #Filter out questions not included in previous_questions array
                questions_raw = (Question.query
                .filter(Question.id.notin_(previous_questions))
                .all())   

            #If all questions are used, return without question to end game
            if len(questions_raw) == 0:
                return jsonify({
                    'success': True,
                })           

            # Format questions & get a random question
            questions_formatted = [question.format() for question in questions_raw]
            random_question = random.choice(questions_formatted)

            return jsonify({
                'success': True,
                'question': random_question,
                'previous_questions': previous_questions
            })

        except:
            # abort unprocessable if error
            abort(422)
  
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
