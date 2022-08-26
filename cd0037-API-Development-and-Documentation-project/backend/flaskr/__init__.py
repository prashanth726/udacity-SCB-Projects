import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


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
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories')
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        print(len(categories))
        if len(categories) == 0:
            abort(404)

        categoriesData = {}
        for category in categories:
            categoriesData[str(category.id)] = category.type

        return jsonify({'categories': categoriesData, 'success': True, 'total_categories': len(categories)})

    @app.route('/questions')
    def get_questions():
        Questions = Question.query.order_by(Question.id).all()
        categories = Category.query.order_by(Category.id).all()
        cuurent_questions = paginate_questions(request, Questions)
        if len(cuurent_questions) == 0:
            abort(404)

        categoriesData = {}
        for category in categories:
            categoriesData[str(category.id)] = category.type

        QuestionsData = []

        for question in Questions:
            QuestionsData.append({'id': question.id, 'question': question.question,
                                 'category': question.category, 'answer': question.answer, 'difficulty': question.difficulty})

        return jsonify({
            'success': True,
            'questions': cuurent_questions,
            'total_questions': len(Questions),
            'categories': categoriesData,
            'current_category': None,
        })

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        # By using the ID get the question from Database
        question = Question.query.filter(Question.id == id).one_or_none()
        if question is None:
            abort(404)
        # Deelte the question
        question.delete()
        return jsonify({
            'success': True,
            'deleted_question_id': id,
            'message': 'Question deleted',
        })

    @app.route('/questions', methods=['POST'])
    def create_question():
        # Get the question and answer text, category, and difficulty score from body
        data = request.get_json()
        if all(key in data for key in ('question', 'answer', 'category', 'difficulty')):
            question = data.get('question')
            answer_text = data.get('answer')
            category = data.get('category')
            difficulty_score = data.get('difficulty')

            # Create new question in database
            created_question = Question(
                question=question, answer=answer_text, category=category, difficulty=difficulty_score)
            Question.insert(created_question)
            return jsonify({
                'success': True,
                'id': created_question.id
            })
        else:
            abort(404)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        data = request.get_json()
        if "searchTerm" in data:
            # Search the question based on search term
            search_term = data.get('searchTerm')
            Questions = Question.query.order_by(Question.id).filter(
                Question.question.ilike('%{}%'.format(search_term))).all()

            if len(Questions) == 0:
                abort(404)

            # Questions to paginate
            current_questions = paginate_questions(request, Questions)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'total_questions': len(Questions),
                'current_category': None,
            })
        else:
            abort(404)

    @app.route('/categories/<int:id>/questions')
    def get_questions_by_category_id(id):
        # Get all the questions based on category.
        Questions = Question.query.filter(Question.category == id).all()
        cuurent_questions = paginate_questions(request, Questions)

        if len(Questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': cuurent_questions,
            'total_questions': len(Questions),
            'current_category': id,
        })

    @app.route('/quizzes', methods=['POST'])
    def get_questions_for_quiz():
        data = request.get_json()
        if all(key in data for key in ('previous_questions', 'quiz_category')):
            previous_questions = data.get('previous_questions')
            quiz_category = data.get('quiz_category')

            if quiz_category['id'] == 0:
                Questions = Question.query.all()
            else:
                Questions = Question.query.filter(
                    Question.category == quiz_category['id']).all()

            QuestionsData = []

            for question in Questions:
                QuestionsData.append({'id': question.id, 'question': question.question,
                                      'category': question.category, 'answer': question.answer, 'difficulty': question.difficulty})

            questions_without_previous_questions = list(
                filter(lambda i: i['id'] not in previous_questions, QuestionsData))

            if len(questions_without_previous_questions) > 0:
                # we found the questions without any previous questions
                return jsonify({
                    'success': True,
                    'question': random.choice(questions_without_previous_questions),
                })
            else:
                # all questions over, so lets end the game
                return jsonify({
                    'success': True,
                    'question': None,
                })
        else:
            abort(404)

  # Error handlers for all expected errors

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404,
                    "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422,
                    "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    return app
