import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(dbURI='', test_config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='postgresql://{}:{}@{}/{}'.format('student','student','localhost:5432', 'trivia')
    )
    if dbURI:
        setup_db(app, dbURI)
    else:
        setup_db(app)
    
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    """
    @Done: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @Done: Use the after_request decorator to set Access-Control-Allow
    """

    @app.route("/categories", methods=['GET'])
    def get_categories():
        # This endpoint serves get requests to return all categories available in the database
        try:
            # ok path: query all categories from database
            categories = Category.query.all()
            categories_formatted = {}
            # loop through all elements of the result and format them --> build up returnbody
            for category in categories:
                to_add = category.format()
                categories_formatted[to_add['id']] = to_add['type']
            # return JSON object containing the formatted categories and the successmessage
            return jsonify({
                "categories": categories_formatted,
                "success": True
                })
        # in case of failure return error 404 (not found)
        except:
            abort(404)
    """
    @Done:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route("/questions", methods=['GET'])
    def get_questions():
        # this endpoint serves get requests to get all questions and categories in the database
        try: 
            pageNr = request.args.get("page",1,int)
            # ok path: query all categories from database
            categories = Category.query.all()
            categories_formatted = {}
            # loop through all elements of the result and format them --> build up returnbody for categories
            for category in categories:
                to_add = category.format()
                categories_formatted[to_add['id']] = to_add['type']
            # query all questions from database and format them
            questions = Question.query.all()
            questions_formatted = [ques.format() for ques in questions]
            # check if request was not on last page
            if len(questions_formatted)>pageNr*QUESTIONS_PER_PAGE:
                questions_paginated = questions_formatted[(pageNr-1)*QUESTIONS_PER_PAGE:pageNr*QUESTIONS_PER_PAGE]
            # check if request was on last page
            elif len(questions_formatted)>(pageNr-1)*QUESTIONS_PER_PAGE:
                questions_paginated = questions_formatted[(pageNr-1)*QUESTIONS_PER_PAGE:]
            # if request was on page behind last page (available pages)
            else:
                abort(404)
            # return requested content
            return jsonify({
                "success": True,
                "categories": categories_formatted,
                "questions": questions_paginated,
                "total_questions": len(questions_formatted),
                "currentCategroy": "ALL"
            })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)



    """
    @Done:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        # This endpoint serves the deletion of a question with the id of the question being handed over
        try:
            questionToDelete = Question.query.get(question_id)
            questionToDelete.delete()
            return jsonify({
                "success": True,
                "id": questionToDelete.id
            })
        except:
            abort(404)
    """
    @Done:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions", methods=["POST"])
    def create_question():
        # This endpoint combines to post-request methods: one to get questions based on a search term and another one to create new questions
        newQuestion = request.get_json()
        if "searchTerm" in newQuestion:
            try:
                pageNr = 1
                questionsThatMatch = Question.query.filter(Question.question.ilike('%'+newQuestion["searchTerm"]+'%'))
                questions_formatted = [ques.format() for ques in questionsThatMatch]
                # check if request was not on last page
                if len(questions_formatted)>pageNr*QUESTIONS_PER_PAGE:
                    questions_paginated = questions_formatted[(pageNr-1)*QUESTIONS_PER_PAGE:pageNr*QUESTIONS_PER_PAGE]
                # check if request was on last page
                elif len(questions_formatted)>(pageNr-1)*QUESTIONS_PER_PAGE:
                    questions_paginated = questions_formatted[(pageNr-1)*QUESTIONS_PER_PAGE:]
                # if request was on page behind last page (available pages)
                else:
                    abort(404)
                # return requested content
                return jsonify({
                    "success": True,
                    "questions": questions_paginated,
                    "total_questions": len(questions_formatted),
                    "currentCategroy": "ALL"
                })
            except:
                abort(400)
        else:
            # This endpoint serves the creation of a question with answer, category and difficulty
            try:
                if (newQuestion["question"] is None or newQuestion["answer"] is None or newQuestion["category"] is None or newQuestion["difficulty"] is None):
                    abort(400)
                questionToAdd = Question(question=newQuestion["question"], answer=newQuestion["answer"], category=newQuestion["category"], difficulty=newQuestion["difficulty"])
                questionToAdd.insert()
                return jsonify({
                    "success": True,
                    "id": questionToAdd.id,
                    "question": questionToAdd.question,
                    "answer": questionToAdd.answer,
                    "difficulty": questionToAdd.difficulty,
                    "category": questionToAdd.category
                })
            except Exception as e:
                if isinstance(e, HTTPException):
                    abort(e.code)
                else:
                    abort(422)
    """
    @Done:
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

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

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
    @app.errorhandler(400)
    def err_bad_request(error):
        return jsonify({
            "success": False,
            "message": "The request was not formatted correctly",
            "error": 400
        }), 400

    @app.errorhandler(404)
    def err_not_found(error):
        return jsonify({
            "success": False,
            "message": "The requested resource could not be found",
            "error": 404
        }), 404
    
    @app.errorhandler(422)
    def err_not_processable(error):
        return jsonify({
            "success": False,
            "message": "The request could not be processed",
            "error": 422
        }), 422
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

