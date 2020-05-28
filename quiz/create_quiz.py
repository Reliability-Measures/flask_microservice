import json
import time
import datetime
import logging
import threading
import socket

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


# extract and process items for quiz
def process_items(results):
    questions = []
    index = 1
    tags = set()
    for result in results:
        metadata = json.loads(result.get('metadata', {}))
        choices = json.loads(result.get('choices', {}))
        topic = result.get('topic')
        tags.add(result.get('subject'))

        desc = metadata.get('quiz', '') + " " + topic
        try:
            topic = json.loads(topic)
            topic.items()
            tags.update(topic.items())
            desc = metadata.get('description') or metadata.get('quiz', '')
        except:
            tags.add(topic)

        item = {
            'question': str(index) + ". " + result.get('text'),
            'description': desc,
            'options': choices,
            'points': metadata.get('points'),
            'type': get_type_from_id(result.get('type'), 'google_form'),
            'feedback_correct': metadata.get('feedback_correct'),
            'feedback_incorrect': metadata.get('feedback_incorrect'),
        }
        # print(item)
        questions.append(item)
        index += 1
    return questions, tags


def create_quiz_thread(title, desc, results, options, user_profile, new_id):
    items = []
    tags = []
    error = None
    searchable = 1
    script_results = {}

    st = time.monotonic()
    try:
        items, tags = process_items(results)
        tags = ','.join(tags)
        # print(tags)
        email_name = options.get('required', 0x02)
        options = {'email': email_name & 0x01, 'name': email_name & 0x02,
                   'show_correct': options.get('show_correct', 0)
                   }
        searchable =  options.get('searchable', searchable)
        credentials = GoogleCredentials().get_credential()
        params = [title, desc, user_profile, items, options]
        # print(params)
        script_results = run_app_script(credentials, function_name='createQuiz',
                                 params=params)
        metadata = script_results.get('metadata', {})
        folder = metadata.get('folder_name')
        form_id = metadata.get('id')
        if form_id and folder:
            params = [form_id, folder]
            run_app_script(credentials, function_name='moveFiles',
                           params=params)
    except Exception as exc:
        logger.error("Quiz creation App Script exception: " + str(exc))
        error = str(exc)

    et = time.monotonic() - st

    # insert/update in DB
    try:
        metadata_quiz = script_results.get('metadata', {})
        metadata_quiz['elapsed'] = et
        if error:
            metadata_quiz['error'] = error
        # user_profile = results.get('user_profile', {})
        values = (new_id, metadata_quiz.get('id'),
                  title, desc,
                  json.dumps(metadata_quiz, indent=4),
                  1, metadata_quiz.get('count_items'),
                  metadata_quiz.get('total_points'),
                  json.dumps(items, indent=4),
                  metadata_quiz.get('published_url'),
                  json.dumps(user_profile, indent=4),
                  user_profile.get('email'), tags, searchable
                  )
        # print("****", values)
        db = MySqlDB()
        db.connect()
        db.insert(insert_sqls[2], values)
    except Exception as exc:
        logger.error("error", exc)


# create quiz from user provided data
def create_quiz_form_db(json_data, sql=None):

    new_id = ''
    try:
        max_id = connect_and_execute("select max(id) as max_id from exams")
        new_id = int(max_id[0].get("max_id")) + 1
        title = json_data.get('quiz_name')
        desc = json_data.get('quiz_description', '')
        ids = json_data.get('item_ids')
        user_profile = json_data.get('user_profile', {})
        options = json_data.get('options', {})
        # create exam in DB
        db = MySqlDB()
        db.connect()
        values = (str(new_id), title, desc)
        db.insert(insert_sqls[3], values)

        # get items
        if not sql:
            sql = queries[11].format(','.join(map(str, ids)))
        results = connect_and_execute(sql)

        # do actual creation in a thread
        if json_data:
            thread = threading.Thread(target=create_quiz_thread,
                                      args=(title, desc, results, options,
                                            user_profile, new_id))
            thread.start()

        return {"quiz": {'quiz_name': title, 'exam_id': new_id}}

    except Exception as exc:
        logger.error("Quiz creation DB exception: " + str(exc))
        return {"quiz": {}, 'error': str(exc)}
    # return {"quiz": results, "error": error, "elapsed": str(et)}


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

    #print(len(results))

    for result in results:
        result['user_profile'] = json.loads(result.get('user_profile') or '{}')
        result['metadata'] = json.loads(result.get('metadata') or '{}')

    if len(results) > 0:
        return {"quiz": results, "quiz_count": len(results)}
    else:
        return {"quiz": "Not found!", "quiz_count": 0}


# sample quiz
def create_quiz(subject='Islam', topic=None):
    q = queries[9]
    sql = q.format(subject, 50)
    if topic:
        sql = queries[10].format(subject, topic, 15)

    results = connect_and_execute(sql)
    # print(json.dumps(results, indent=4))
    items, tags = process_items(results)
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


def create_quiz_sample(json_data):
    limit = json_data.get('limit', 25)

    # SCRIPT_ID = "1PGHEjAEw4GeNCd_LfmrmclpU4E9_rnq9vhcO6mzYMzSFpF0Ylr_bNVq3"
    sql = "select id, text, subject, topic, sub_topics, type, choices, " \
          "metadata, answer from items where subject='Islam' limit " + \
          str(limit)
    options = {'required': 0x03, 'show_correct': 0, 'summary': 1}
    user = {'email': 'farrukh503@gmail.com', 'givenName': 'Farrukh'}

    results = create_quiz_form_db({'quiz_name': 'test',
                                   'options': options,
                                   'user_profile': user},
                                  sql=sql)

    return results


if __name__ == '__main__':
    st = time.monotonic()
    initialize_config()


    # print(json.dumps(create_quiz(topic='Seerah'), indent=4))
    # http://api2.reliabilitymeasures.com/create_form/?input={"quiz_description":"Test","quiz_name":"Form 1","item_ids":[2,45,6,9,25]}
    # http://api2.reliabilitymeasures.com/get_items/?input={"subject":"Islam","limit":10}

    ids = [1, 3, 6, 9, 25]
    # ids = [131,132]
    json_data = {'quiz_description': 'Test main', 'quiz_name': 'Form main',
                 'item_ids': ids, 'options':{}}
    #print(json.dumps(create_quiz_form_db(json_data), indent=4))

    # json_data = {'user_id': "farrukh503@gmail.com", 'limit': 10}
    # print(json.dumps(get_quiz_form_db(json_data), indent=4,
    #                 default=decimal_default))

    #json_data = {'subject': "", 'limit': 5, "user_id": ""}
    #print(json.dumps(get_items_db(json_data), indent=4))

    # sql = queries[11].format(','.join(map(str, ids)))
    # print(sql)
    # res = connect_and_execute(sql)
    # print(json.dumps(res, indent=4))

    #print(create_quiz_sample({}))

    json_data = {'id': 98, 'name': 'test'}
    json_data = {'keyword': '2020'}
    print(json.dumps(search_quiz(json_data), indent=4,
                     default=decimal_default))

    et = time.monotonic() - st
    print(et)
