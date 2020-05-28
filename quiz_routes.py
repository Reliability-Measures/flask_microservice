import json
from flask.blueprints import Blueprint
from flask_cors import CORS

from process_requests import process_request
from quiz.create_item import insert_item
from quiz.create_quiz import create_quiz_form_db,  create_quiz_sample
from quiz.get_quiz import get_items_db, get_quiz_form_db,  \
    search_quiz, get_quiz_responses

quiz_app = Blueprint('quiz_app', __name__)

CORS(quiz_app)

@quiz_app.route('/item/', methods=['POST'])
@quiz_app.route('/create_item/', methods=['POST'])
def put_item():
    return process_request(insert_item)


@quiz_app.route('/get_items/', methods=['POST', 'GET'])
def get_items():
    return process_request(get_items_db)


@quiz_app.route('/get_items_sample', methods=['POST', 'GET'])
def get_items_sample():
    return process_request(
        get_items_db,
        json.dumps({'subject': 'Islam', 'topic': 'Aqeedah'})
    )


@quiz_app.route('/create_form/', methods=['POST', 'GET'])
def create_form():
    return process_request(create_quiz_form_db)


@quiz_app.route('/create_form_sample/', methods=['POST', 'GET'])
def create_form_sample():
    return process_request(create_quiz_sample,  '{}')


@quiz_app.route("/quiz_account/", methods=['POST', 'GET'])
def quiz_account():
    return process_request(get_quiz_form_db)


@quiz_app.route('/get_form/', methods=['POST', 'GET'])
def get_form():
    return process_request(search_quiz)


@quiz_app.route('/get_responses/', methods=['POST', 'GET'])
def get_responses():
    return process_request(get_quiz_responses)
