from flask import Flask, request, jsonify
from flask_cors import cross_origin, CORS
from flask.json import JSONEncoder
import json
import sys
import logging

from quiz_routes import quiz_app
from classroom_routes import classroom_app

from common.config import get_config, initialize_config
from common.sample import sample
from api.std import calculate_std
from api.summation import calculate_summation
from api.proportion import calculate_proportion
from api.kr20 import calculate_kr20
from api.idr import calculate_idr ,calculate_idr_average
from api.difficulty import calculate_difficulty, calculate_difficulty_average
from api.scores import calculate_scores, calculate_average
from api.analyze_test import analyze_test
from api.weighted_scores import calculate_weighted_scores, \
    calculate_weighted_average
from api.excludes import get_exclude_recos
from api.num_correct import calculate_num_correct
from api.assumptions import get_assumptions
from api.analyze_groups import analyze_groups
from api.topic_rights import calculate_topic_rights, calculate_topic_averages

from process_requests import process_request
from quiz.quiz_queries import decimal_default


class RMApp(Flask):

    def __init__(self, *args, **kwargs):
        super(RMApp, self).__init__(*args, **kwargs)
        initialize_config()


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        return decimal_default(obj)


app = RMApp(__name__)
app.register_blueprint(quiz_app)
app.register_blueprint(classroom_app)

app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True
CORS(app)
app.json_encoder = CustomJSONEncoder

logger = logging.getLogger(__name__)


@app.errorhandler(Exception)
def unhandled_exception(e):
    logger.error('Unhandled Exception: %s, %s' % (str(e), request.path))
    return index(str(e), 500)


@cross_origin()
@app.route('/', methods=['POST', 'GET'])
def index(error=None, code=200):
    resp = {
            "message": "Welcome from Reliability Measures!",
            "version": get_config('application_version'),
            'python_version': sys.version.split()[0],
            "route": request.path,
            "status_code": code
    }
    if error:
        resp["error"] = error
    return jsonify(resp)


@app.route('/std/', methods=['POST', 'GET'])
def compute_std():
    return process_request(calculate_std)


@app.route('/summation/', methods=['POST', 'GET'])
def compute_summation():
    return process_request(calculate_summation)


@app.route('/proportion/', methods=['POST', 'GET'])
def compute_proportion():
    return process_request( calculate_proportion)


@app.route('/kr20/', methods=['POST', 'GET'])
def compute_kr20():
    return process_request(calculate_kr20)


@app.route('/idr/', methods=['POST', 'GET'])
def compute_idr():
    return process_request( calculate_idr)


@app.route('/difficulty/', methods=['POST', 'GET'])
def compute_difficulty():
    return process_request(calculate_difficulty)


@app.route('/scores/', methods=['POST', 'GET'])
def compute_scores():
    return process_request(calculate_scores)


@app.route('/average/', methods=['POST', 'GET'])
def compute_average():
    return process_request(calculate_average)


@app.route('/analyzeTest/', methods=['POST', 'GET'])
def get_analysis():
    return process_request(analyze_test)


@app.route('/weightedScores/', methods=['POST', 'GET'])
def compute_weighted_scores():
    return process_request( calculate_weighted_scores)


@app.route('/weightedAverage/', methods=['POST', 'GET'])
def compute_weighted_avg():
    return process_request( calculate_weighted_average)


@app.route('/excludes/', methods=['POST', 'GET'])
def compute_excludes():
    return process_request(get_exclude_recos)


@app.route('/difficulty_avg/', methods=['POST', 'GET'])
def compute_diff_avg():
    return process_request(calculate_difficulty_average)


@app.route('/idr_avg/', methods=['POST', 'GET'])
def compute_idr_avg():
    return process_request( calculate_idr_average)


@app.route('/num_correct/', methods=['POST', 'GET'])
def compute_num_correct():
    return process_request( calculate_num_correct)


@app.route('/assumptions/', methods=['POST', 'GET'])
def compute_assumptions():
    return process_request( get_assumptions)


@app.route('/analyze_groups/', methods=['POST', 'GET'])
def get_group_analysis():
    return process_request( analyze_groups)


@app.route('/topic_rights/', methods=['POST', 'GET'])
def get_topic_rights():
    return process_request( calculate_topic_rights)


@app.route('/topic_averages/', methods=['POST', 'GET'])
def get_topic_averages():
    return process_request(calculate_topic_averages)


@app.route('/sample', methods=['POST', 'GET'])
@app.route('/sample/', methods=['POST', 'GET'])
def get_sample_analysis():
    return process_request(analyze_test, json.dumps(sample))


if __name__ == '__main__':
    print("Starting service")
    app.run(host="0.0.0.0", port=5000, threaded=True)

