import json
from flask import request, jsonify
from flask.blueprints import Blueprint
from flask_cors import CORS

from common.config import get_config
from quiz.quiz_queries import get_query_result, \
    get_quizzes_by_names
from providers.google.get_credentials import GoogleCredentials
from providers.google.google_classroom import list_courses, \
    list_students_teachers

classroom_app = Blueprint('classroom_app', __name__)
CORS(classroom_app)


@classroom_app.route('/login/', methods=['POST', 'GET'])
def get_tokens():
    id_token = request.args.get('id_token')
    access_token = request.args.get('access_token')
    gc = GoogleCredentials()
    creds, info = gc.get_credential_from_token(id_token, access_token)
    courses = list_courses(creds)
    return jsonify({'user': info, 'courses': courses})


@classroom_app.route('/classroom/', methods=['POST', 'GET'])
def get_classes():
    id_token = request.args.get('id_token')
    access_token = request.args.get('access_token')

    gc = GoogleCredentials()
    if access_token and id_token:
        creds, info = gc.get_credential_from_token(id_token, access_token)
    else:
        creds = gc.get_credential()  # RM organization courses
        info = {'name': get_config("application_org"),
                'email': get_config("application_email")}

    courses = list_courses(creds)
    return jsonify({'user': info, 'courses': courses})


@classroom_app.route('/classroom/people', methods=['POST', 'GET'])
def get_people():
    course_id = request.args.get('course_id')
    people = request.args.get('people', 0)  # students by default
    gc = GoogleCredentials()
    creds = gc.get_credential()  # RM organization courses

    result = list_students_teachers(creds,
                                    teachers=bool(people),
                                    course_id=course_id)
    return jsonify(result)


@classroom_app.route('/quiz/', methods=['POST', 'GET'])
def get_quiz():
    name = request.args.get('name')
    stat = request.args.get('stat')
    age = request.args.get('age')
    ignore_case = bool(request.args.get('ignore_case', 'true'))
    all_responses = bool(request.args.get('all_responses', 'true'))
    if stat:
        results = get_query_result(id=stat)
    else:
        results = get_quizzes_by_names(name, ignore_case, all_responses, age)
    return jsonify(results)

