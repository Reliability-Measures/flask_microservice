import json

from providers.myssql_db import MySqlDB
from common.config import initialize_config
from quiz.subjects import subjects as subjects_json
from quiz.type_map import get_type_id
from quiz.quiz_queries import insert_sqls


# function to process the question from UI
def insert_item(item_data):
    sql = insert_sqls[0]
    sql2 = insert_sqls[1]

    tags = item_data.get('tags')
    private = tags.get('privacy', 0)

    # Getting choices and answer
    item_choices = item_data.get('item_choices', [])
    choice_list = []
    answer_list = []
    for i in item_choices:
        choice_list.append(i.get('choice', ''))
        if i.get('correct') == 1:
            answer_list.append(i.get('choice'))
    choices = json.dumps(choice_list, indent=4)
    answers = json.dumps(answer_list, indent=4)

    user_profile = item_data.get('user_profile', {})

    # Getting metadata
    metadata = json.dumps(item_data, indent=4)

    # Getting type info
    item_type = get_type_id(tags.get('item_type'))

    # Getting subject, topic, and hierarchy info
    subject_list = subjects_json.get('subject_list')
    paths = tags.get('paths')
    subject = tags.get('subject')
    subject_id = None
    topic = None
    topic_id = None
    sub_topics = None
    sub_ids = None
    if paths is not None:
        topic = {}
        topic_id = {}
        sub_topics = {}
        sub_ids = {}
        for sub in subject_list:
            if sub.get('label') == subject:
                subject_id = sub.get('subject_id')
                break

        index = 0
        for path in paths:
            curr_topic = None
            curr_topic_id = None
            curr_sub_topics = None
            curr_sub_ids = None
            path = path.replace('children.', '')
            split_path = path.split('.')
            del split_path[0]
            if split_path:
                curr_topic_id = int(split_path[len(split_path)-1])
                del split_path[len(split_path)-1]
            if split_path:
                curr_sub_ids = list(map(int, split_path))

            for i in subject_list:
                if i.get('subject_id') == subject_id:
                    if curr_sub_ids:
                        curr_sub_topics = []
                        children = i.get('children')
                        for j in curr_sub_ids:
                            for k in children:
                                if j == children.index(k):
                                    child = children[j]
                                    curr_sub_topics.append(child.get('label'))
                                    children = child.get('children')
                                    break
                        for j in children:
                            if curr_topic_id == children.index(j):
                                curr_topic = j.get('label')
                    elif curr_topic_id:
                        children = i.get('children')
                        for j in children:
                            if curr_topic_id == children.index(j):
                                curr_topic = j.get('label')
                                break
                    break

            topic[index] = curr_topic
            topic_id[index] = curr_topic_id
            sub_topics[index] = curr_sub_topics
            sub_ids[index] = curr_sub_ids
            index += 1

        topic = json.dumps(topic)
        topic_id = json.dumps(topic_id)
        sub_topics = json.dumps(sub_topics)
        sub_ids = json.dumps(sub_ids)

    values = (tags.get('id', ''), tags.get('item_text', ''),
              subject, subject_id, topic,
              topic_id, sub_topics, sub_ids, item_type,
              metadata, choices, answers)

    db = MySqlDB()
    db.connect()

    values2 = (tags.get('id', ''), tags.get('item_text', ''),
               subject, subject_id, topic,
               topic_id, sub_topics, sub_ids, item_type,
               metadata, json.dumps(item_choices, indent=4), answers,
               json.dumps(user_profile, indent=4),
               user_profile.get('email'), private
               )

    db.insert(sql2, values2)
    return {'response': db.insert(sql, values)}


if __name__ == '__main__':
    initialize_config()
    item = {
      "user_profile":{
          "googleId": "xxxx",
          "imageUrl": "yyy",
          "email": "info@reliabilitymeasures.com",
          "name": "reliabilitymeasures.com",
          "givenName": "Reliability Measures"
      },
      "tags": {
        "item_text": "123123123",
        "subject": "Biology",
        "item_type": "Multiple Choice",
        "grade_min": "1",
        "grade_max": "12",
        "privacy": 1,
        "paths": [
          "1.children.1"
        ]
      },
      "item_choices": [
        {
          "correct": 0,
          "choice": "123"
        },
        {
          "correct": 1,
          "choice": "123"
        },
        {
          "correct": 0,
          "choice": "123123"
        },
        {
          "correct": 0,
          "choice": "234234"
        }
      ]
    }

    insert_item(item)
    #sql = "SELECT * FROM `questions`"
    #db = MySqlDB()
    #db.connect()
    # db.query("TRUNCATE TABLE `questions`", False)
    #print(db.query(sql, True))
