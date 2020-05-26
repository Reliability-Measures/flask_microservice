import json
import logging

from common.config import initialize_config
from quiz.quiz_queries import queries, connect_and_execute, insert_sqls, \
    decimal_default
from providers.google.google_run_app_script import run_app_script, \
    GoogleCredentials
from quiz.type_map import get_type_from_id
from providers.myssql_db import MySqlDB

logger = logging.getLogger(__name__)


def get_quiz_form_db(json_data):
    user_id = json_data.get('user_id')
    limit = json_data.get('limit', 1000)

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


# returns items from DB for specific filters
def get_items_db(json_data):
    subject = json_data.get('subject')
    topic = json_data.get('topic')
    limit = json_data.get('limit', 50)
    #keyword = json_data.get('keyword')
    user_id = json_data.get('user_id', "")

    sql = queries[9].format(subject, limit)
    if len(user_id) > 2:
        sql = queries[7].format(subject, limit, user_id)
    if topic:
        sql = queries[10].format(subject, topic, limit)
        if len(user_id) > 2:
            sql = queries[8].format(subject, topic, limit, user_id)

    #print(sql)
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


# extract and process items for quiz
def process_items(results):
    questions = []
    index = 1
    for result in results:
        metadata = json.loads(result.get('metadata', {}))
        choices = json.loads(result.get('choices', {}))
        topic = result.get('topic')
        desc = metadata.get('quiz', '') + " " + topic
        try:
            topic = json.loads(topic)
            desc = metadata.get('description') or metadata.get('quiz', '')
        except:
            pass
        item = {
            'question': str(index) + ". " + result.get('text'),
            'description': desc,
            'options': choices,
            'points': metadata.get('points'),
            'type': get_type_from_id(result.get('type'), 'google_form'),
            'feedback_correct': metadata.get('feedback_correct'),
            'feedback_incorrect': metadata.get('feedback_incorrect'),
        }
        #print(item)
        questions.append(item)
        index += 1
    return questions


# create quiz from user provided data
def create_quiz_form_db(json_data):
    items = []
    user_profile = {}
    try:
        title = json_data.get('quiz_name')
        desc = json_data.get('quiz_description')
        ids = json_data.get('item_ids')
        user_profile = json_data.get('user_profile')
        options = json_data.get('options')

        # get items from list of ids
        sql = queries[11].format(','.join(map(str, ids)))
        results = connect_and_execute(sql)
        items = process_items(results)
        email_name = options['required']
        options = {'email': email_name & 0x01, 'name': email_name & 0x02,
                   'show_correct': options.get('show_correct', 0)}
        creds = GoogleCredentials().get_credential()
        params = [title, desc, user_profile, items, options]
        results = run_app_script(creds, function_name='createQuiz',
                                 params=params)
    except Exception as exc:
         logger.error("Quiz creation exception: " + str(exc))
         return {"quiz": {}, 'error': str(exc)}

    # insert in DB
    exc = None
    try:
        metadata_quiz = results.get('metadata')
        # user_profile = results.get('user_profile', {})
        values = ('', metadata_quiz.get('id'),
                  results.get('title'),
                  results.get('description'),
                  json.dumps(metadata_quiz, indent=4),
                  1, metadata_quiz.get('count_items'),
                  metadata_quiz.get('total_points'),
                  json.dumps(items, indent=4),
                  metadata_quiz.get('published_url'),
                  json.dumps(user_profile, indent=4),
                  user_profile.get('email')
                  )
        # print("****", values)
        db = MySqlDB()
        db.connect()
        db.insert(insert_sqls[2], values)
    except Exception as exc:
        logger.error("error", exc)
        pass

    return {"quiz": results, "error": str(exc)}


# sample quiz
def create_quiz(subject='Islam', topic=None):
    q = queries[9]
    sql = q.format(subject, 50)
    if topic:
        sql = queries[10].format(subject, topic, 15)

    results = connect_and_execute(sql)
    # print(json.dumps(results, indent=4))
    items = process_items(results)
    user = json.loads(results[0].get('metadata', {}))
    user = user.get('user_profile')
    pt = "We are compiling the results for 25 Quizzes. " \
         "Please complete any missed ones before the 29th of Ramadan.\n\n" \
         "We are very grateful for your overwhelming response, " \
         "support and feedback to our daily Ramadan quizzes. " \
         "Ramadan will shortly be over but our striving to gain knowledge " \
         "should continue. We will soon be introducing a feature to allow " \
         "you to contribute your own questions and create your own quizzes. " \
         "Please look out for more updates on this soon."

    creds = GoogleCredentials().get_credential()
    options = {'email': 0, 'name': 1, 'show_correct': 1}
    params = ['Ramadan 2020 Quiz Review 7',
              "All " + topic + " Questions (" + str(len(results)) + "). "
              "See all quizzes here: http://muslimscholars.info/quiz/\n\n" + pt,
              user, items, options]
    return run_app_script(creds, function_name='createQuiz', params=params)


if __name__ == '__main__':
    initialize_config()

    #print(json.dumps(create_quiz(topic='Seerah'), indent=4))
    # http://api2.reliabilitymeasures.com/create_form/?input={"quiz_description":"Test","quiz_name":"Form 1","item_ids":[2,45,6,9,25]}
    # http://api2.reliabilitymeasures.com/get_items/?input={"subject":"Islam","limit":10}

    #ids = [1, 3, 6, 9, 25]
    #ids = [131,132]
    #json_data = {'quiz_description': 'Test', 'quiz_name': 'Form 2',
    #             'item_ids': ids}
    #print(json.dumps(create_quiz_form_db(json_data), indent=4))

    #json_data = {'user_id': "farrukh503@gmail.com", 'limit': 10}
    #print(json.dumps(get_quiz_form_db(json_data), indent=4,
    #                 default=decimal_default))

    json_data = {'subject': "",  'limit': 5, "user_id": ""}
    print(json.dumps(get_items_db(json_data), indent=4))

    # sql = queries[11].format(','.join(map(str, ids)))
    # print(sql)
    # res = connect_and_execute(sql)
    # print(json.dumps(res, indent=4))
