from flask import request, jsonify
import json

from quiz.quiz_queries import decimal_default


def process_request(fn, json_data=None):
    """
    A function to convert a JSON formatted string to dict and
    then call the passed function and return the response.

    :param fn: a function to call
    :param json_data: str (optional in JSON format)
    :return: str, a JSON formatted string
    """
    pretty_json = 1
    try:
        pretty_json = request.args.get('pretty', pretty_json)
        if not json_data:
            json_data = request.args.get('input') or request.args.get('json')
        # print(pretty_json, json_data)
        inp = json.loads(json_data)

        ans = fn(inp)  # calling function 'fn'
        print(ans)
        ans['Input'] = inp
    except Exception as exc:
        ans = {"error": str(exc), 'input': json_data}
    if pretty_json == 1:
        return jsonify(ans)
    else:
        return json.dumps(ans, default=decimal_default)
