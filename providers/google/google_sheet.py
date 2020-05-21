import json
import time
from datetime import datetime

from googleapiclient.discovery import build
from providers.google.get_credentials import GoogleCredentials
from providers.myssql_db import MySqlDB
from providers.google.google_run_app_script import run_app_script
from common.config import initialize_config

quiz_links = [
    "https://docs.google.com/forms/d/e/1FAIpQLScWsZp2hHvaK1T3ClRXYiYnbxE5np48EjI7dRua3uAqJYyRLQ/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSePfn6rVDPSnlzPwZ-J4iT-I8Etdnma0zr2sJGNbvk9W9itXQ/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSdpSo8mekRI7jScqNtfuX_nUBOpOGnuuARkR1b8wSvDB26nsw/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSel8jWSvqc0jinJwsCQ2mJNDQ5zPsV1a4esQRA5GkXz-iKFdw/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSesHSSk1u_4zhiKXo3-lUgfjlTn6ikA9wmVDT7YcQp1ezZlgQ/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSe7xCDXY--JZD8dssvW1lK1fSlOYh9GULE7uxYF6d4EUZ7P1Q/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfgniIGN07J7Mb3pYqS0BGNMJ2SOpWrTA8_gVCimcb25NC1FA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSerQjGhaU1oAtZXNNvwgOAaogGpRzLErF8lAKntKCqHoZePbg/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfhW7pZ2oHsPZngvSOydJ0VpfVVgEbtedW01JaQVtNHnbLgGw/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfnLwbUmRt2_l-b0uVH8BVnYDHPl9cDIN_sf6QwzCC9KvIEHg/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSdstQSpDJgDtHUqLH7g2T7HYq1-yivr24u_U0-FyVZ3QfY9KA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSf0StazPDOJsUP94S0TiFG-zaIwLtQk_cM3oHFGohY8qus-yA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfkUt8oABZNsp5NhWYwSm8ZdxSqzTahvNcw8Gd7HJUdDfMr-Q/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSerk_I5wnlbccm0DF3V4Aki3FxG07YvJXNriFiOnng3ElEK6g/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfREh-kwG56ARUeIYqqYQk3i6NPZT_Cf4lyFpr5MinhM-U7uA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSekPY3BgHr2Qbp-Snv8pC1Ge-79xaf15K3SL1rAAfCp6xLbJA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfrE1mlxJ3ABLddoKU87ica8YbwMHap9JPSDsxtItAsDoyiPA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSeTBjhMU9J4KskMHFS-kHEzHZYNRoU7jiruUwf_NRYbKC8rMA/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSfStls1KxaIDrjWGNMLrA_tbd-OA2IlIXw6v2EfXkl_Ys2aDw/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSc5KPE7yb8hu5-_MpZ8i87UC84SLAUJKIocGS6AMUpuQUrIgQ/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSf27hpXbxiem626bCMVQzKN0T_1EfxQVUp3_8d3itM3tdqsFg/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLScBou4QKNcBr7yXbwEhxcNGIk6J0QowKTEPx_uJ5ja8NtiOJw/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSdKH3BiypPpap5e62-mk2ONl8vqz1HJaPHbmFYDGvkuIE9www/viewform",
    "https://docs.google.com/forms/d/e/1FAIpQLSe67Nak0k70l8Yzxnl8shff15u344NNrwLwXi1uU8KA8uFuRg/viewform?usp=sf_link",
    "https://docs.google.com/forms/d/e/1FAIpQLSdSHMgGFf5nMJ8MLqdz1B4UVZ3BkNw0bG4RKMd2PxiZHA5ptA/viewform?usp=sf_link"
]

QUIZES = ['1wxJ2TAM75oPu_JM8g6OfHHmq-Zy2K4H0hj3RzEoWrko',
          '1YqKgwDOcaXV18ndcmFxUi74mtzbVDMC9EXOIRxenQ6M',
          '1bGPWCeTQDO2fvMrmm8qsVqc9HrtDUvgjz3uEHYosI5U',
          '1ap2RTfete16Q76KWefeM8TF59XjVugzF-unGTJOk85k',
          '1BR88xMigzYiA_eN3h5S-8sUI1QIDwAs02gfuuanJ13o',
          '1Z75Hg9k3TTMF4ZPSMOMn_2Ccs5wHsbkxBU_MHMWOEo8',
          '1l6dRb24i38a1Lcy3qrGpnKErnjhyNqMh2kiq_V01vsk',
          '1yGlgUxZmnDLMHk-8qN86OLEEVp-M4zUZLXFFPab_PXw',
          '1uuWQ7wz3GbyegY-YF2qz4RNVh1yAosvDDZEaKauKpyY',
          '16Kh0jZNmRXlnnat-RJiu0ssL6uaav5OKM_Ran5xeDqA',
          '1PuTHHfVh75OyxYdYfrefUexJcR01nBX4FU8h5VC-3ps',
          '1PFpwrmL9xOrgJ0OztwyDin8YXpORA0vgG_JYl3_fmrI',
          '1MfmZ9xpe3D_QLPAYk0R-_v3oF9wHNf-ljwdRWT2KbQU',
          '1hKwnTaLQ96Qn5SeNnU58Lo58Q9C3fRqOOhJj3JPyEAI',
          '1gckVo4zHSLt5okHteOBnjg9evU0mtR4aujjiKLIs-G4',
          '1ogFFuUcMYzBoiqT8jQWGz8WuFGxTyFlsShPvhRR0aEM',
          '1HMBOOhOQqY08wIJhU7mowqsoW_twAEIQAHKRQjg5DuI',
          '1b85yUdBkMR2oUnurBwTKcmCUwPnwi1Az7HpjrhtTAZY',
          '1bnLWVv8nlAUIuuagWnQCFAabdW6x7fi1WI0sH65dgpk',
          '1gZTh2GYZxgL4VWmH2qlBx0KLgBoulXM7tYMNKqydUvU',
          '1HdTosObBNpC1n84SooWCL_iByaNKJPeC3VhyLmgKIV0',
          '1rrpinZ2RgKnR8PPxzahYwr3l7Sc_BvseDtHtjDzbQOo',
          '1MwB2ZJ_Uops4g59p3PsOF1ChscM6amZRlxwP9zt26-E',
          '1LjyKKi-Nsn5uFtrWOEBsl5PBnNfAbnQRJ0YoGByUV3I',
          '12DOYvBCBIxfKKtSZ0dlS4Yalf-i0oS8YAe_TnWHF484'
          ]

topics_new = ['Aqeedah', 'Qur`an', 'Fiqh', 'Seerah', 'History']
topics1 = ['History', 'Aqeedah', 'Seerah', 'Fiqh', 'Qur`an']
topics2 = ['Seerah', 'Fiqh', 'Qur`an', 'Qur`an', 'Seerah']
topics3 = ['Aqeedah', 'Qur`an', 'Fiqh', 'Fiqh', 'Qur`an']
topics_25 = ['Aqeedah', 'Aqeedah', 'Qur`an', 'Qur`an', 'Fiqh', 'Fiqh',
             'Seerah', 'Seerah', 'History', 'History']

item_type = {'undefined': 0, 'multiple choice': 1}

del_dup = """select * from students where name in (
SELECT name
FROM students where description = 'Quiz 2' 
GROUP BY name
HAVING COUNT(*) > 1) and description = 'Quiz 2' order by name"""


def datetime_format(datestr, fr="%m/%d/%Y %H:%M:%S", to="%Y-%m-%d %H:%M:%S"):
    dt = datetime.strptime(datestr, fr)
    return datetime.strftime(dt, to)


def get_sheet(creds=None, sheet_id=None, col_range=None):
    if not creds:
        creds = GoogleCredentials().get_credential_local()

    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id,
                                range=col_range).execute()
    values = result.get('values', [])

    #gs = sheet.get(spreadsheetId=sheet_id)
    #print(gs)

    return values


if __name__ == '__main__':
    sql_quiz = "INSERT INTO quizzes(`id`, `provider_id`, `name`, " \
               "`description`, `metadata`, `type`, `no_of_questions`, " \
               "`total_marks`, `questions`, `timestamp`, `responses`, " \
               "`external_link`) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql_ques = "INSERT INTO `quiz_questions`(`id`, `text`, `subject`, " \
               "`topic`, `type`, `metadata`, `choices`, `answer`) " \
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    sql_responses = "INSERT INTO `students`(`id`, `creation_date`,`marks`, `name`, " \
                  "`description`,`age`, `city`, `state`, " \
                  "`school`, `responses`) VALUES " \
                  "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    initialize_config()
    creds = GoogleCredentials().get_credential_local()
    db = MySqlDB()
    # print(db)
    db.connect()

    print(db.query("show tables"))
    print(db.query_commit("delete from quizzes"))
    print(db.query_commit("delete from students"))
    print(db.query_commit("delete from quiz_questions"))
    print(db.query_commit("ALTER TABLE students AUTO_INCREMENT=1"))
    print(db.query_commit("ALTER TABLE quiz_questions AUTO_INCREMENT=1"))

    close = 0
    q_type = item_type['multiple choice']
    index = 1

    for quiz in QUIZES[index-1:]:
        rows = get_sheet(creds, sheet_id=quiz,
                              col_range="Form Responses 1")
        print("Quiz ", index, quiz, len(rows))
        head = rows[0]
        answers = rows[1]
        choices = []

        questions = []
        correct_answers = []
        metadata = []
        topic_list = [topics1, topics2, topics3]
        topics = topics_new
        if index <= 3:
            topics = topic_list[index - 1]
        start = 5
        end = 10
        count = 5
        if index == 25:
            end = 15
            count = 10
            topics = topics_25

        for h in head[:start]:
            metadata.append(h)

        for h in head[start:end]:
            questions.append(h)

        for a in answers[start:end]:
            if index == 12 and a == 'D) All of the above':
                a += ";E) A and B only"
            correct_answers.append(a)
            choices.append(set())

        # get all responses
        all_responses = []
        for row in rows[1:]:
            i = 0
            loc = row[4].strip()
            location = loc.replace(',', '/').split('/')
            values = ('', datetime_format(row[0]), row[1], row[2].strip(),
                      'Quiz ' + str(index), row[3],
                      location[0].strip(), )
            if len(location) > 1:
                values += (location[1].strip(),)
            else:
                values += (location[0].strip(),)
            if len(location) > 2:
                values += (location[2].strip(),)
            else:
                values += (location[0].strip(),)

            responses = []
            for a in row[start:end]:
                choices[i].add(a)
                responses.append(a)
                i += 1
            values += (json.dumps(responses), )
            #print(values)
            all_responses.append(values)

        print(db.insert(sql_responses, all_responses))

        # change and sort all set() to list for json
        options = []
        for ch in choices:
            op = list(sorted(ch))
            print(len(op), op)
            options.append(op)

        ques_dict = {'questions': questions,
                     'correct_answers': correct_answers,
                     'choices': options,
                     'topics': topics
                     }
        values = (index, quiz, 'Quiz ' + str(index), '', json.dumps(metadata),
                  q_type, len(head[:start]), count, json.dumps(ques_dict),
                  datetime_format(answers[0]), len(rows)-1,
                  quiz_links[index - 1])

        #print(sql_quiz + str(values))

        print(db.insert(sql_quiz, values))
        metadata = {'timestamp': datetime_format(answers[0]),
                    'quiz': 'Quiz ' + str(index),
                    'weight': 1,
                    'external_link': quiz_links[index - 1]}
        for q, c, o, t in zip(questions, correct_answers, options, topics):
            values = ('', q, 'Islam', t, q_type, json.dumps(metadata),
                      json.dumps(o), json.dumps(c))
            print(values)
            print(db.insert(sql_ques, values))

        index += 1

        time.sleep(5)