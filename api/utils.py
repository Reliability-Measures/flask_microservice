from statistics import pstdev
from api.config import get_keyword_value


def get_item_std(item):
    scoreList = []
    for i in item:
        score = sum(i)
        scoreList.append(score)
    # scoreSTD = get_std(scoreList)  # micro service call
    scoreSTD = pstdev(scoreList)

    return scoreSTD


def get_id_list(param):
    inp = update_input(param)
    student_list = get_student_list(inp)
    idList = []
    responseList = []
    
    for i in student_list:
        responseList.append(i[get_keyword_value("item_responses")])
        
    for i in responseList:
        for k in i:
            curr_id = int(k[get_keyword_value("item_id")])
            if curr_id not in idList:
                idList.append(curr_id)
    
    idList.sort()

    return idList


def get_sorted_responses(param):
    inp = update_input(param)
    student_list = get_student_list(inp)
    numStudents = len(student_list)
    idList = get_id_list(inp)
    responseList = []
    responses = {}
    
    for i in student_list:
        responseList.append(i[get_keyword_value("item_responses")])

    for i in idList:  # Create a dictionary with the item IDs as keys
        responses[i] = []
    
    for i in responseList:  # For each student response list i
        checklist = idList.copy()
        for k in i: # For each question k
            for j in responses: # For each item ID j
                # If item IDs match, add response to dictionary
                if k[get_keyword_value("item_id")] == j:
                    responses[j].append(k[get_keyword_value("response")])
                    checklist.remove(j)

        if len(checklist) != 0:
            for i in checklist:
                responses[i].append(0)

    sortedResponses = []
    for i in range(0, numStudents):  # For each student
        studentResponses = []
        for k in responses: # For every item ID
            # Create a list of the students responses sorted by item ID
            studentResponses.append(responses[k][i])
        sortedResponses.append(studentResponses)

    return sortedResponses


def get_grad_year_list(param):
    inp = update_input(param)
    student_list = get_student_list(inp)
    grad_year_list = []
        
    for i in student_list:
        curr_grad_year = i.get(get_keyword_value("grad_year"))
        if curr_grad_year != None:
            if curr_grad_year not in grad_year_list:
                grad_year_list.append(curr_grad_year)
    
    grad_year_list.sort()

    return grad_year_list


def sort_students_by_grad_year(param):
    inp = update_input(param)
    student_list = get_student_list(inp)
    grad_year_list = get_grad_year_list(inp)
    id_list = get_id_list(inp)
    responses_by_grad_year = {}

    for i in grad_year_list:
        responses_by_grad_year[i] = {(get_keyword_value("student_list")): []}

    for i in grad_year_list:
        for k in range(0, len(student_list)): 
            curr_item_ids = []
            curr_responses = student_list[k][get_keyword_value("item_responses")]
            for j in curr_responses:
                curr_item_ids.append(j[get_keyword_value("item_id")])
            for j in id_list:
                if j not in curr_item_ids:
                    student_list[k][get_keyword_value("item_responses")].append({get_keyword_value("item_id"): j, get_keyword_value("response"): 0})
            if student_list[k][get_keyword_value("grad_year")] == i:
                responses_by_grad_year[i][get_keyword_value("student_list")].append(student_list[k])

    return responses_by_grad_year


def get_student_list(param):
    inp = update_input(param)
    student_list = list(inp[get_keyword_value("student_list")])

    return student_list


def update_input(param):
    inp = param
    student_list = list(param[get_keyword_value("student_list")])
    exclude_students = list(param.get(get_keyword_value("exclude_students"), []))
    exclude_items = list(param.get(get_keyword_value("exclude_items"), []))
    remove_students = []

    for i in range(0, len(student_list)):
        curr_stud = student_list[i].get(get_keyword_value("id"))
        if curr_stud is None:
            student_list[i][(get_keyword_value("id"))] = i+1

    for i in range(0, len(student_list)):
        curr_responses = student_list[i][get_keyword_value("item_responses")]
        for k in range(0, len(curr_responses)):
            curr_item = curr_responses[k].get(get_keyword_value("item_id"))
            if curr_item is None:
                student_list[i][get_keyword_value("item_responses")][k][get_keyword_value("item_id")] = k+1

    for i in student_list:
        if int(i[get_keyword_value("id")]) in exclude_students:
            remove_students.append(i)
    for i in remove_students:
        student_list.remove(i)

    for i in range(0, len(student_list)):
        remove_items = []
        curr_responses = student_list[i][get_keyword_value("item_responses")]
        for k in curr_responses:
            curr_item = k[get_keyword_value("item_id")]
            if curr_item in exclude_items:
                remove_items.append(k)
        for k in remove_items:
            curr_responses.remove(k)
        student_list[i][get_keyword_value("item_responses")] = curr_responses

    inp[get_keyword_value("student_list")] = student_list
    return inp