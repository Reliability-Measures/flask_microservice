from api.utils import get_item_std, get_sorted_responses, get_student_list, update_input
from api.config import get_service_config, get_keyword_value


def calculate_kr20(param):
    service_key = get_service_config(1)
    inp = update_input(param)
    student_list = {get_keyword_value("student_list"): get_student_list(inp)}
    sortedResponses = get_sorted_responses(student_list)
    numStudents = len(sortedResponses)
    numItems = len (sortedResponses[0])
    pqList = []
    scoreSTD = get_item_std(sortedResponses)

    if scoreSTD <= 0:
        return {service_key: get_keyword_value("bad_std")}

    for i in range(0, numItems):
        p = 0
        for k in range(0, numStudents):
            p += sortedResponses[k][i]
        p /= numStudents
        q = 1 - p
        pqList.append(p * q)
    pqSum = sum(pqList)

    # need validation here
    kr20_value = (numItems /(numItems - 1)) * (1 - (pqSum / (scoreSTD ** 2)))

    return {service_key: round(kr20_value, 3)}