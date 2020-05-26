"""
Shows basic usage of the Apps Script API.

"""
import json
from googleapiclient import errors
from googleapiclient.discovery import build

from providers.google.get_credentials import GoogleCredentials
from common.config import initialize_config
from providers.myssql_db import MySqlDB

SCRIPT_ID = '1FJi_cMqS8i1g5tvDMZa7qC60NW0vWSDf4pIOeggLSt5eIwbuPuyjJrB2'


def run_app_script(credentials=None, script_id=SCRIPT_ID,
                   function_name="myFunction",
                   params=None):
    """Calls the Apps Script API.
    """
    # store = oauth_file.Storage('token2.json')
    # creds = store.get()
    # if not creds or creds.invalid:
    #     flow = client.flow_from_clientsecrets('client.json', SCOPES)
    #     creds = tools.run_flow(flow, store)

    if not credentials:
        credentials = GoogleCredentials().get_credential_local()
    service = build('script', 'v1', credentials=credentials)

    # Call the Apps Script API
    result = []
    try:
        # Create an execution request object.
        request = {"function": function_name, "parameters": params}
        response = service.scripts().run(body=request,
                                         scriptId=script_id).execute()

        # print("..................")

        if 'error' in response:
            # The API executed, but the script returned an error.

            # Extract the first (and only) set of error details. The values of
            # this object are the script's 'errorMessage' and 'errorType', and
            # an list of stack trace elements.
            error = response['error']['details'][0]
            print("Script error message: {0}".format(error['errorMessage']))

            if 'scriptStackTraceElements' in error:
                # There may not be a stacktrace if the script didn't start
                # executing.
                print("Script error stacktrace:")
                for trace in error['scriptStackTraceElements']:
                    print("\t{0}: {1}".format(trace['function'],
                                              trace['lineNumber']))
        else:
            # The structure of the result depends upon what the Apps Script
            # function returns.
            result = response['response'].get('result', {})
            if not result:
                print('No result returned!')
            #else:
            #    print("Result: ", result)

    except errors.HttpError as e:
        # The API encountered a problem before the script started executing.
        print("ERROR", e.content)
        result = {'error': e.content}

    return result


if __name__ == '__main__':
    from quiz.type_map import get_type_id
    initialize_config()
    creds = GoogleCredentials().get_credential_local()
    db = MySqlDB()
    db.connect()

    print(db.query_commit("delete from exams"))
    print(db.query_commit("delete from items"))
    print(db.query_commit("ALTER TABLE items AUTO_INCREMENT=1"))
    topics_new = ['Aqeedah', 'Qur`an', 'Fiqh', 'Seerah', 'History']
    topics1 = ['History', 'Aqeedah', 'Seerah', 'Fiqh', 'Qur`an']
    topics2 = ['Seerah', 'Fiqh', 'Qur`an', 'Qur`an', 'Seerah']
    topics3 = ['Aqeedah', 'Qur`an', 'Fiqh', 'Fiqh', 'Qur`an']
    topics_25 = ['Aqeedah', 'Aqeedah', 'Qur`an', 'Qur`an', 'Fiqh', 'Fiqh',
                 'Seerah', 'Seerah', 'History', 'History']
    quiz_links = [
        {'quiz': 'Islamic Quiz 1',
         'link': "https://docs.google.com/forms/d/1psEEWT9X0VfmKjE97OrYza3vnYsHyZWMkqhGkMB5N-I/edit"},
        {'quiz': 'Islamic Quiz 2',
         'link': "https://docs.google.com/forms/d/1tcpyuVpRZ7a2LpubcstPLoKenBNSCa4W5U0HScepR8M/edit"},
        {'quiz': 'Islamic Quiz 3',
         'link': "https://docs.google.com/forms/d/1hfr0gYey6Ppx1v3TFeD1i3je7FD16Vi81GNH3s0NnH4/edit"},
        {'quiz': 'Islamic Quiz 4',
         'link': "https://docs.google.com/forms/d/1hEhs_a3R60_ZqbDrf4jriIeZv0azvNTpYFTFdgEiFYA/edit"},
        {'quiz': 'Islamic Quiz 5',
         'link': "https://docs.google.com/forms/d/1Yv4nRvN8muj7_WQkWkmhzBmj8WtBZBaFHrxI-WA5oI0/edit"},
        {'quiz': 'Islamic Quiz 6',
         'link': "https://docs.google.com/forms/d/1XN7XS9D-ERLh9FJxNC6CJyoj2ZFVA0E8ajSJJfvfr2A/edit"},
        {'quiz': 'Islamic Quiz 7',
         'link': "https://docs.google.com/forms/d/1iw32wwPUk-0CxyY-ljKi7oqgeeLjH1jJrYrt3sR6XiI/edit"},
        {'quiz': 'Islamic Quiz 8',
         'link': "https://docs.google.com/forms/d/1i8hM9CGVFFZRbZHxleDdUbplfL1SxiQe8GmJZ-klpKs/edit"},
        {'quiz': 'Islamic Quiz 9',
         'link': "https://docs.google.com/forms/d/1-ZqklLDv0sm1enuCObxTJgxE3kOYl-WmDXHsipUjalU/edit"},
        {'quiz': 'Islamic Quiz 10',
         'link': "https://docs.google.com/forms/d/1I2FafY9YqNwvtsVnwA_WPDjuFVL8WxLUlpJgKp4MCBA/edit"},
        {'quiz': 'Islamic Quiz 11',
         'link': "https://docs.google.com/forms/d/1-xvpY6Z8VAyW3tTLdKD6jwuMgth-YsMP6GNbBRcdBdw/edit"},
        {'quiz': 'Islamic Quiz 12',
         'link': "https://docs.google.com/forms/d/1dF8UnzD-pcmQUqu8CtF5CeFlsiKkHO4CyMotxEaK8T4/edit"},
        {'quiz': 'Islamic Quiz 13',
         'link': "https://docs.google.com/forms/d/1wrPdT2UNdEwOcZg9mPvYE9X-CF1j-620TgJBI92avxQ/edit"},
        {'quiz': 'Islamic Quiz 14',
         'link': "https://docs.google.com/forms/d/1GFJ9ArW0oNUaEPe2GZjAZAbySzVkrIcYoQ1WNpY0z7U/edit"},
        {'quiz': 'Islamic Quiz 15',
         'link': "https://docs.google.com/forms/d/1dsm3NZ4NuwaI86F2k2cuJQR7x8Y-snc3ZOMP204pNLQ/edit"},
        {'quiz': 'Islamic Quiz 16',
         'link': "https://docs.google.com/forms/d/1rlwAmNrZmd2OuW79I6sf8CwLCJpsplHVTAnbV5QYCwo/edit"},
        {'quiz': 'Islamic Quiz 17',
         'link': "https://docs.google.com/forms/d/1bwT7VoX_6SD22TdvOySqBtWE7ACV9A2QzkUwtgHsxd4/edit"},
        {'quiz': 'Islamic Quiz 18',
         'link': "https://docs.google.com/forms/d/1IwByAkcyEsGZmuNTZKCavfQ2GxAPvr4_20wC-wnOCa0/edit"},
        {'quiz': 'Islamic Quiz 19',
         'link': "https://docs.google.com/forms/d/1YCZrH6hwcarGcl7u2ZgiZZUkZq3FfKgDlJc70EtcaKA/edit"},
        {'quiz': 'Islamic Quiz 20',
         'link': "https://docs.google.com/forms/d/1Osk4V_cUjIk_Hs_dwk4iHhrmfqvnkEFE2TgiGl4JVJk/edit"},
        {'quiz': 'Islamic Quiz 21',
         'link': "https://docs.google.com/forms/d/1Kgv4w0cwSiqREZHkxsDT7YVfpU-PTYuz4OneAfBpv-I/edit"},
        {'quiz': 'Islamic Quiz 22',
         'link': "https://docs.google.com/forms/d/1L17t8-CDQq0G_Mcj2czcy1_xOz0-8c5tg4Xe2b0-lI4/edit"},
        {
            'quiz': 'Islamic Quiz 23',
            'link': "https://docs.google.com/forms/d/1-OepgpNqVpHU45OE_Sn4IZJAviOCF_E_Jd1wkTt2pHM/edit"
        },
        {
            'quiz': 'Islamic Quiz 24',
            'link': "https://docs.google.com/forms/d/1eJgoRzOq00jv2D32Jyav7o6cElJ9sdORU_oUrJQj69c/edit"
        },
        {
            'quiz': 'Islamic Quiz 25',
            'link': "https://docs.google.com/forms/d/1Lm78M2TWNct_DWKY2DKS8gQNKxBUcL2nBt7fxg8XvHU/edit"
        },
        ]

    quiz_links =[
        {'link': "https://docs.google.com/forms/d/1Np8ZS9kT0JJ3-aV8Uf-_wfTmn_y37zMMj7lnZS6Pjrk/edit",
         'quiz': 'Algebra 2'}
    ]

    subject = "Islam"
    subject_id = 5
    topic_list = [topics1, topics2, topics3]

    sql_quiz = "INSERT INTO exams(`id`, `provider_id`, `name`, " \
               "`description`, `metadata`, `type`, `no_of_questions`, " \
               "`total_marks`, `questions`, `timestamp`, `responses`, " \
               "`external_link`) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_ques = "INSERT INTO `items`(`id`, `text`, `subject`, `subject_id`, " \
               "`topic`, `type`, `metadata`, `choices`, `answer`, " \
               "`user_profile`, `user_id`, " \
               "`timestamp_created`, `timestamp_updated`) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    index = 1


    topic_list = [['History', 'Aqeedah', 'Seerah', 'Fiqh', 'Qur`an']]

    user_profile = {"googleId": "xxxx",
                    "imageUrl": "yyy",
                    "email": "info@reliabilitymeasures.com",
                    "name": "reliabilitymeasures.com",
                    "givenName": "Reliability Measures"
                    }

    for q in quiz_links[index-1:]:
        if index <= 3:
            topics = topic_list[index - 1]
        else:
            topics = topics_new
        if index == 25:
            topics = topics_25

        quiz = q['link']
        quiz_name = q['quiz']
        params = [quiz, False]
        results = run_app_script(creds, function_name='getQuizDetails',
                                 params=params)
        print(json.dumps(results, indent=4))
        metadata_quiz = results.get('metadata')
        updated = metadata_quiz.get('updated')

        i = 0
        other_fields = []
        questions = []
        correct_answers = []
        for item in results.get('items'):
            if not item.get('points') or \
                    (item.get('type') not in ['CHECKBOX', 'MULTIPLE_CHOICE']):
                other_fields.append(item.get('title'))
                continue

            questions.append(item.get('title'))
            answer = item.get('answer')
            if index == 12 and answer == 'D) All of the above':
                answer += ";E) A and B only"
            correct_answers.append(answer)
            metadata = {
                'timestamp': updated,
                'quiz': results.get('title'),
                'description': item.get('description'),
                'points': item.get('points'),
                'feedback_correct': item.get('feedback_correct'),
                'feedback_incorrect': item.get('feedback_incorrect')
            }
            # choices = {
            #     'options': item.get('choices'),
            #     'corrects': item.get('corrects')
            # }
            text = item.get('title')
            # remove no.
            arr = text.split(".", 1)
            if len(arr[0]) < 3:
                text = arr[1].strip()

            values = ('', text, subject, subject_id,
                      topics[i], get_type_id(item.get('type')),
                      json.dumps(metadata, indent=4),
                      json.dumps(item.get('choices'), indent=4),
                      json.dumps([answer], indent=4),
                      json.dumps(user_profile, indent=4),
                      user_profile.get('email'),
                      results.get('created'), updated
                      )
            # print(values)
            i += 1
            print(db.insert(sql_ques, values))
        metadata_quiz['other_fields'] = other_fields
        metadata_quiz['user_profile'] = user_profile
        questions = {
            'questions': questions,
            'correct_answers': correct_answers,
            'topics': topics,
            'items': results.get('items')
        }
        values = (index, metadata_quiz.get('id'),
                  results.get('title'),
                  results.get('description'),
                  json.dumps(metadata_quiz, indent=4),
                  1, metadata_quiz.get('count_items'),
                  metadata_quiz.get('total_points'),
                  json.dumps(questions, indent=4),
                  updated, results.get('responses_count'),
                  metadata_quiz.get('published_url'))
        print(values)
        print(db.insert(sql_quiz, values))
        index += 1
