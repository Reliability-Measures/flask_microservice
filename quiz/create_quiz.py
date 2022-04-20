import json
import time
import socket
import logging
import threading

from common.config import initialize_config
from quiz.quiz_queries import queries, connect_and_query, insert_sqls, \
     connect_and_execute, delete_sqls
from providers.google.google_run_app_script import run_app_script, \
    GoogleCredentials
from quiz.type_map import get_type_from_id


logger = logging.getLogger(__name__)


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
            for t in topic.items():
                if t[1]:
                    tags.add(t[1])
            desc = metadata.get('description') or metadata.get('quiz', '')
        except:
            tags.add(topic)

        item_type = get_type_from_id(result.get('type'), 'google_form')
        count_correct = 0
        for choice in choices:
            count_correct += int(choice.get('correct') or 0)

        if count_correct > 1:  # Checkboxes
            item_type = get_type_from_id(1, 'google_form')
        item = {
            'question': str(index) + ". " + result.get('text'),
            'description': desc,
            'options': choices,
            'points': metadata.get('points'),
            'type': item_type,
            'feedback_correct': metadata.get('feedback_correct'),
            'feedback_incorrect': metadata.get('feedback_incorrect'),
        }
        # print(item)
        questions.append(item)
        index += 1
    return questions, list(tags)


def create_quiz_thread(title, desc, results, options, user_profile, new_id):
    items = []
    tags = []
    error = None
    searchable = 1
    script_results = {}

    st = time.monotonic()
    try:
        items, tags = process_items(results)
        tags = str(','.join(tags))
        #print(tags)
        email_name = options.get('required', 0x02)
        searchable = options.get('searchable', searchable)
        options = {'email': email_name & 0x01, 'name': email_name & 0x02,
                   'show_correct': options.get('show_correct', 0)
                   }

        credentials = GoogleCredentials().get_credential()
        params = [title, desc, user_profile, items, options]
        socket.setdefaulttimeout(180)
        script_results = run_app_script(credentials,
                                        function_name='createQuiz',
                                        params=params)
        metadata = script_results.get('metadata', {})
        folder = metadata.get('folder_name')
        form_id = metadata.get('id')
        if form_id and folder:
            params = [form_id, folder]
            run_app_script(credentials,
                           function_name='moveFiles',
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
                  user_profile.get('email'), tags, str(searchable)
                  )
        # print("****", values)
        connect_and_execute(insert_sqls[2], values)
    except Exception as exc:
        logger.error("error", exc)


# create quiz from user provided data
def create_quiz_form_db(json_data, sql=None):

    new_id = ''
    try:
        max_id = connect_and_query("select max(id) as max_id from exams")
        new_id = int(max_id[0].get("max_id")) + 1
        title = json_data.get('quiz_name')
        desc = json_data.get('quiz_description', '')
        ids = json_data.get('item_ids')
        user_profile = json_data.get('user_profile', {})
        options = json_data.get('options', {})
        # create exam in DB
        values = (str(new_id), title, desc)
        connect_and_execute(insert_sqls[3], values)

        # get items
        if not sql:
            sql = queries[11].format(','.join(map(str, ids)))
        results = connect_and_query(sql)

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


# sample quiz
def create_quiz(subject='Islam', topic=None):
    q = queries[9]
    sql = q.format(subject, 50)
    if topic:
        sql = queries[10].format(subject, topic, 15)

    results = connect_and_query(sql)
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

    #sql = delete_sqls[1].format(','.join(map(str, [163,164, 165, 166])))
    #print(sql)
    #connect_and_query(sql)

    ids = [484, 479, 476, 474, 458]
    #sql = queries[11].format(','.join(map(str, [306, 2])))
    #print(sql)

    #results = connect_and_query(sql)
    #print(json.dumps(results, indent=4))

    #exit(0)

    # ids = [131,132]
    user = {'email': 'info@reliabilitymeasures.com', "givenName": "Reliability Measures"}
    json_data = {'quiz_description': '''Jazak Allah Khair for participating in these Ramadan quizzes.
See All quizzes for this year here: https://muslimscholars.info/Ramadan2022/
''',

                 'quiz_name': 'Ramadan 1443/2022 Quiz 19',
                 'user_profile': user,
                 'item_ids': ids,
                 'options': {'email': 0, 'name': 1, 'show_correct': 1}}
    # json_data = {'quiz_description': '''We are very grateful for your overwhelming response, support and feedback to our daily Ramadan quizzes.
    #     Overall, we received about 4000 entries. This is the last quiz for this Ramadan.
    # See previous quizzes here: https://muslimscholars.info/Ramadan2021/
    #
    # الْلَّهُمَّ اِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي''',
    #
    #              'quiz_name': 'Ramadan 2021/1442 Quiz 25',
    #              'user_profile': user,
    #              'item_ids': ids,
    #              'options': {'email': 0, 'name': 1, 'show_correct': 1}}
    print(json.dumps(create_quiz_form_db(json_data), indent=4))

    # json_data = {'user_id': "farrukh503@gmail.com", 'limit': 10}
    # print(json.dumps(get_quiz_form_db(json_data), indent=4,
    #                 default=decimal_default))

    #json_data = {'subject': "", 'limit': 5, "user_id": ""}
    #print(json.dumps(get_items_db(json_data), indent=4))

    # sql = queries[11].format(','.join(map(str, ids)))
    # print(sql)
    # res = connect_and_query(sql)
    # print(json.dumps(res, indent=4))

    #print(create_quiz_sample({}))

    et = time.monotonic() - st
    print(et)
