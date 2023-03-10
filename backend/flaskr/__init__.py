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
    
    # set up CORS
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # decorater to set access-control allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

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

    @app.route("/questions", methods=["POST"])
    def create_question():
        # This endpoint combines to post-request methods: one to get questions based on a search term and another one to create new questions
        newQuestion = request.get_json()
        # Go into search stream 
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
            # This route serves the creation of a question with answer, category and difficulty
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

    @app.route("/categories/<int:category_id>/questions")
    def get_questions_from_category(category_id):
        # This endpoint returns all questions belonging to a category id
        try:
            category = Category.query.filter(Category.id==category_id).one_or_none()
            # check if category exists
            if category is None:
                abort (404)
            # get all questions to existing category
            questions = Question.query.filter(Question.category == category_id).all()
            questions_formatted = [ques.format() for ques in questions]
            # return object
            return jsonify({
                "success": True,
                "current_category": category_id,
                "total_questions": len(questions_formatted),
                "questions": questions_formatted
            })
        # errorhandling
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.route("/quizzes", methods=["POST"])
    def play_quiz():
        try:
            inputData = request.get_json()
            indexesUsed = inputData.get("previous_questions")
            if inputData.get("quiz_category").get("id") == 0:
                questions = Question.query.all()
            else:
                category = Category.query.filter(Category.id==inputData.get("quiz_category").get("id")).one_or_none()
            # check if category exists
                if category is None:
                    abort (404)
                #get all questions of category and filter for the ones that have not been posted yet
                questions = Question.query.filter(Question.category==inputData.get("quiz_category").get("id")).all()
                questions_formatted = [ques.format() for ques in questions]
                questions_unused = [ques for ques in questions_formatted if ques["id"] not in indexesUsed]
                # check if any questions are left and send response
                if len(questions_unused) != 0:
                    question_return = random.choice(questions_unused)
                    return jsonify({
                        "success": True,
                        "question": question_return
                    })
                else: 
                    return jsonify({
                        "success": True,
                        "question": False
                    })
        except Exception as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)
        
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
    
    @app.errorhandler(500)
    def err_internal(error):
        return jsonify({
            "success": False,
            "message": "Something went wrong on serverside",
            "error": 500
        }), 500

    return app

