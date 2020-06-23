from quiz.create_item import insert_item
"""
get data from

https://umich.instructure.com/files/2330198/download?download_frd=1&verifier=hwdEj267RR86WHe2zORgLKOpCfUXBA6HOaG2xNVQ

"""


# Plan: convert questions from site into same format as 'aws CCL sample exam.txt' with scraper, then run this function.
def create_items_from_file():
    questions = []
    answers = []
    f = open("aws CCL sample exam.txt", "r")
    reached_ans = False
    i = 0
    item = {
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
            if i == 5:
                questions.append(item)
                item = {
                    "tags": {
                        "item_text": "",
                        "item_type": "Multiple Choice",
                        "subject": "AWS"
                    },
                    "item_choices": []
                }
                i = 0
            if i == 0:
                item['tags']['item_text'] = line.split(') ')[1].replace('\n', '')
                i += 1
            elif i < 5:
                item['item_choices'].append({'choice': line.split(') ')[1].replace('\n', ''), 'correct': 0})
                i += 1
        else:
            answers.append(ord(line.split(') ')[1][0])-65)

    for i in questions:
        ans = answers[questions.index(i)]
        i['item_choices'][ans]['correct'] = 1

    f.close()
    return questions


items = create_items_from_file()
for i in items:
    insert_item(i)
