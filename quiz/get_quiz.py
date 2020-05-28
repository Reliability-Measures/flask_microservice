import json
import time
import logging
import socket


from api.analyze_test import analyze_test
from common.config import initialize_config
from quiz.quiz_queries import queries, connect_and_execute, decimal_default
from providers.google.google_run_app_script import run_app_script, \
    GoogleCredentials

logger = logging.getLogger(__name__)


#  returns items from DB for specific filters
def get_items_db(json_data):
    subject = json_data.get('subject')
    topic = json_data.get('topic')
    limit = json_data.get('limit', 50)
    # keyword = json_data.get('keyword')
    user_id = json_data.get('user_id', "")

    sql = queries[9].format(subject, limit)
    if len(user_id) > 2:
        sql = queries[7].format(subject, limit, user_id)
    if topic:
        sql = queries[10].format(subject, topic, limit)
        if len(user_id) > 2:
            sql = queries[8].format(subject, topic, limit, user_id)

    # print(sql)
    results = connect_and_execute(sql)
    results = sorted(results, key=lambda pos: pos['id'])

    for result in results:
        result['choices'] = json.loads(result.get('choices', {}))
        result['metadata'] = json.loads(result.get('metadata', {}))
        try:
            result['topic'] = json.loads(result['topic'])
            result['sub_topics'] = json.loads(result['sub_topics'])
        except:
            pass
        result['answer'] = json.loads(result.get('answer', {}))

    return {'items': results, 'total_items': len(results)}


def get_quiz_form_db(json_data):
    user_id = json_data.get('user_id')
    limit = json_data.get('limit', 100)

    # get all items by user
    sql = queries[12].format(user_id, limit)
    items = connect_and_execute(sql)
    for item in items:
        item['choices'] = json.loads(item.get('choices', {}))
        item['metadata'] = json.loads(item.get('metadata', {}))
        try:
            item['topic'] = json.loads(item['topic'])
            item['sub_topics'] = json.loads(item['sub_topics'])
        except:
            pass
    # get all quizzes by user
    sql = queries[13].format(user_id, limit)
    exams = connect_and_execute(sql)
    for item in exams:
        item['metadata'] = json.loads(item.get('metadata', {}))

    return {"items": items, "exams": exams,
            "items_count": len(items), "exams_count": len(exams)}


def search_quiz(json_data):
    id = json_data.get('id')
    name = json_data.get('name')
    keyword = json_data.get('keyword')
    results = []
    if id and name:
        sql = queries[14].format(id, name)
        results = connect_and_execute(sql)
    if keyword:
        sql = queries[15].format(keyword)
        results = connect_and_execute(sql)

    for result in results:
        result['user_profile'] = json.loads(result.get('user_profile') or '{}')
        result['metadata'] = json.loads(result.get('metadata') or '{}')

    if len(results) > 0:
        return {"quiz": results, "quiz_count": len(results)}
    else:
        return {"quiz": "Not found!", "quiz_count": 0}


def get_quiz_responses(json_data):
    edit_url = json_data.get('edit_url')
    params = [edit_url]
    credentials = GoogleCredentials().get_credential()
    socket.setdefaulttimeout(180)
    results = run_app_script(credentials,
                             function_name='getQuizResponses',
                             params=params)
    responses = results.get('responses', [])
    # TODO Convert to json format needed for Item Analysis
    # Call Analyze_test and send analysis data in the below dict
    exam_info = {'exam': {'name': results.get('title')}, 'student_list': []}

    for i in results.get('students'):
        curr_id = str(i[0].get('student_id'))
        exam_info['student_list'].append({'id': curr_id, 'item_responses': []})

    for i in results.get('responses'):
        for k in i:
            for j in exam_info['student_list']:
                if str(k.get('student_id')) == j['id']:
                    j['item_responses'].append({'item_id': str(k.get('item_id')), 'response': k.get('score')})

    quiz_analysis = analyze_test(exam_info)['analysis']

    return {"quiz_responses": results, 'quiz_analysis': quiz_analysis}


if __name__ == '__main__':
    st = time.monotonic()
    initialize_config()

    # json_data = {'user_id': "farrukh503@gmail.com", 'limit': 10}
    # print(json.dumps(get_quiz_form_db(json_data), indent=4,
    #                 default=decimal_default))

    #json_data = {'subject': "", 'limit': 5, "user_id": ""}
    #print(json.dumps(get_items_db(json_data), indent=4))


    json_data = {'id': 98, 'name': 'test'}
    json_data = {'keyword': '2020'}
    #print(json.dumps(search_quiz(json_data), indent=4,
    #                 default=decimal_default))

    json_data = {'edit_url': 'https://docs.google.com/forms/d/1DEUSZfBvcZIaL4c255z6boYHrNhcbg6A93JQqvUNUzY/edit'}
    # json_data = {"edit_url": "https://docs.google.com/forms/d/1-OepgpNqVpHU45OE_Sn4IZJAviOCF_E_Jd1wkTt2pHM/edit"}
    results = get_quiz_responses(json_data)
    print(json.dumps(results, indent=4,
                     default=decimal_default))
    # responses = results.get("quiz_responses")
    # print("Items:", len(responses.get('items')))
    # print("Students:", len(responses.get('students')))
    # print("Responses:", len(responses.get('responses')))

    et = time.monotonic() - st
    print(et)
