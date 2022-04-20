import json
import time
import logging
import socket


from api.analyze_test import analyze_test
from common.config import initialize_config, get_config
from quiz.quiz_queries import queries, connect_and_query, decimal_default
from providers.google.google_run_app_script import run_app_script, \
    GoogleCredentials

logger = logging.getLogger(__name__)


#  returns items from DB for specific filters
def get_items_db(json_data):
    subject = json_data.get('subject')
    topic = json_data.get('topic')
    keyword = json_data.get('keyword')
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
    if keyword:
        sql = queries[18].format(subject, keyword, limit)
        if len(user_id) > 2:
            sql = queries[19].format(subject, keyword, limit, user_id)

    # print(sql)
    results = connect_and_query(sql)
    results = sorted(results, key=lambda pos: pos['id'])

    for result in results:
        answer = result.get('answer', {})
        result['choices'] = json.loads(result.get('choices', {}))
        result['metadata'] = json.loads(result.get('metadata', {}))
        try:
            result['topic'] = json.loads(result['topic'])
            result['sub_topics'] = json.loads(result['sub_topics'])
        except:
            pass
        result['answer'] = json.loads(answer)

    return {'items': results, 'total_items': len(results)}


def get_quiz_form_db(json_data):
    user_id = json_data.get('user_id')
    user_profile = json_data.get('user_profile', {})
    limit = json_data.get('limit', 500)

    user_email = user_profile.get('email') or user_id
    user_id = user_profile.get('googleId')

    # get all items by user
    sql = queries[12].format(user_email, limit)
    # get all items for admin
    if user_email in get_config("admin_users") and \
            user_id in get_config("admin_user_ids"):
        sql = queries[16].format(limit)

    items = connect_and_query(sql)
    for item in items:
        item['choices'] = json.loads(item.get('choices', {}))
        item['metadata'] = json.loads(item.get('metadata', {}))
        try:
            item['topic'] = json.loads(item['topic'])
            item['sub_topics'] = json.loads(item['sub_topics'])
        except:
            pass

    # get all quizzes by user
    sql = queries[13].format(user_email, limit)
    # for admin, get all quizzes
    if user_email in get_config("admin_users") and \
            user_id in get_config("admin_user_ids"):
        sql = queries[17].format(limit)

    exams = connect_and_query(sql)
    for item in exams:
        item['metadata'] = json.loads(item.get('metadata') or '{}')
        item['user_profile'] = json.loads(item.get('user_profile') or '{}')
        #print(item.get('analysis'))
        item['analysis'] = json.loads(item.get('analysis') or '{}')

    return {"items": items,
            "exams": exams,
            "items_count": len(items),
            "exams_count": len(exams)}


def search_quiz(json_data):
    id = json_data.get('id')
    name = json_data.get('name')
    keyword = json_data.get('keyword')
    results = []
    if id and name:
        sql = queries[14].format(id, name)
        results = connect_and_query(sql)
    if keyword:
        sql = queries[15].format(keyword)
        results = connect_and_query(sql)

    for result in results:
        result['user_profile'] = json.loads(result.get('user_profile') or '{}')
        result['metadata'] = json.loads(result.get('metadata') or '{}')

    if len(results) > 0:
        return {"quiz": results, "quiz_count": len(results)}
    else:
        return {"quiz": "Not found!", "quiz_count": 0}


def get_quiz_responses(json_data):
    edit_url = json_data.get('edit_url')
    provider_id = json_data.get('provider_id')
    responses = json_data.get('responses')
    params = [edit_url or provider_id, int(responses)]
    credentials = GoogleCredentials().get_credential()
    socket.setdefaulttimeout(300)
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

    for i in responses:
        for k in i:
            for j in exam_info['student_list']:
                if str(k.get('student_id')) == j['id']:
                    j['item_responses'].append({
                        'item_id': str(k.get('item_id')),
                        'response': k.get('score')})

    quiz_analysis = analyze_test(exam_info)['analysis']

    return {"quiz_analysis": quiz_analysis}


if __name__ == '__main__':
    st = time.monotonic()
    initialize_config()

    print(get_config("admin_users"))
    print(get_config("admin_user_ids"))

    user_profile = {"googleId": '117366695156565046594', "email": "info@reliabilitymeasures.com"}
    json_data = {'user_id': "info@reliabilitymeasures.com", 'limit': 10,
                 'user_profile': user_profile}
    print(json.dumps(get_quiz_form_db(json_data), indent=4,
                     default=decimal_default))

    json_data = {'subject': "Islam", 'limit': 50, "user_id": "",
                 "keyword": "fiqh"}
    #print(json.dumps(get_items_db(json_data), indent=4))

    json_data = {'id': 98, 'name': 'test'}
    json_data = {'keyword': '2020'}
    #print(json.dumps(search_quiz(json_data), indent=4,
    #                 default=decimal_default))

    #json_data = {'edit_url': 'https://docs.google.com/forms/d/1DEUSZfBvcZIaL4c255z6boYHrNhcbg6A93JQqvUNUzY/edit'}
    #json_data = {"edit_url": "https://docs.google.com/forms/d/1-OepgpNqVpHU45OE_Sn4IZJAviOCF_E_Jd1wkTt2pHM/edit"}
    #results = get_quiz_responses(json_data)
    #print(json.dumps(results, indent=4,
    #                 default=decimal_default))
    # responses = results.get("quiz_responses")
    # print("Items:", len(responses.get('items')))
    # print("Students:", len(responses.get('students')))
    # print("Responses:", len(responses.get('responses')))

    et = time.monotonic() - st
    print(et)
