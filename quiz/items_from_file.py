from quiz.create_item import insert_item
"""
get data from

https://umich.instructure.com/files/2330198/download?download_frd=1&verifier=hwdEj267RR86WHe2zORgLKOpCfUXBA6HOaG2xNVQ

"""


# Plan: convert questions from site into same format as 'aws CCL sample exam.txt' with scraper, then run this function.
def create_items_from_file(file):
    questions = []
    answers = []
    f = open(file, "r")
    reached_ans = False
    got_question = False
    item = {
        "user_profile": {
            "googleId": "",
            "imageUrl": "",
            "email": "info@reliabilitymeasures.com",
            "name": "reliabilitymeasures.com",
            "givenName": "Reliability Measures"
        },
        "tags": {
            "item_text": "",
            "item_type": "Multiple Choice",
            "subject": "AWS"
        },
        "item_choices": []
    }

    for line in f:
        if line == 'Answers\n':
            questions.append(item)
            reached_ans = True
        elif not reached_ans:
            if line == '\n':
                questions.append(item)
                item = {
                    "user_profile": {
                        "googleId": "",
                        "imageUrl": "",
                        "email": "info@reliabilitymeasures.com",
                        "name": "reliabilitymeasures.com",
                        "givenName": "Reliability Measures"
                    },
                    "tags": {
                        "item_text": "",
                        "item_type": "Multiple Choice",
                        "subject": "AWS"
                    },
                    "item_choices": []
                }
                got_question = False
            elif not got_question:
                item['tags']['item_text'] = line.split(') ')[1].replace('\n', '')
                got_question = True
            else:
                item['item_choices'].append({'choice': line.split(') ')[1].replace('\n', ''), 'correct': 0})
        else:
            answers.append(ord(line.split(') ')[1][0].upper())-65)

    for j in questions:
        ans = answers[questions.index(j)]
        j['item_choices'][ans]['correct'] = 1

    f.close()
    return questions


items = create_items_from_file("sanfoundry1.txt")
for i in items:
    insert_item(i)
