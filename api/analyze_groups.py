from common.config import get_service_config, get_keyword_value
from common.utils import sort_students_by_group, get_student_list, get_group_list, update_input, get_error
from api.kr20 import calculate_kr20
from api.idr import calculate_idr, calculate_idr_average
from api.difficulty import calculate_difficulty, calculate_difficulty_average
from api.scores import calculate_scores, calculate_average
from api.weighted_scores import calculate_weighted_scores, calculate_weighted_average
from api.excludes import get_exclude_recos
from api.num_correct import calculate_num_correct
from api.assumptions import get_assumptions
from api.topic_rights import calculate_topic_rights, calculate_topic_averages


def analyze_groups(param):
    """
    A function to get an exam's analysis by 
    students' group:
    It groups all students by group and 
    then iterates over the groups, calling
    every service used to analyze an exam. 

    :param: a json in the Reliabilty Measures
            standard json format
    :return: a dictionary of nested dictionaries:
             a dictionary with groups as
             keys and the exam analysis as values
    """
    service_key = get_service_config(14)
    catch_error = get_error(param)
    if catch_error[0]:
        return {service_key: catch_error[1]}
    inp = update_input(param)
    assumptions_key = get_service_config(13)
    assumptions = get_assumptions(inp)[assumptions_key]
    students_dict = sort_students_by_group(inp)
    group_list = get_group_list(inp)
    group_analysis = {}

    if group_list == get_keyword_value("no_group"):
        return {service_key: get_keyword_value("no_group")}

    for i in students_dict:
        curr_students = students_dict[i]
        catch_error = get_error(curr_students)
        if catch_error[0]:
            group_analysis[i] = catch_error[1]
            continue
        student_list = get_student_list(curr_students)

        val_kr20 = calculate_kr20(curr_students)
        val_idr = calculate_idr(curr_students)
        val_difficulty = calculate_difficulty(curr_students)
        val_scores = calculate_scores(curr_students)
        val_average = calculate_average(curr_students)
        val_weighted_s = calculate_weighted_scores(curr_students)
        val_weighted_avg = calculate_weighted_average(curr_students)
        val_excludes = get_exclude_recos(curr_students)
        val_diff_avg = calculate_difficulty_average(curr_students)
        val_idr_avg = calculate_idr_average(curr_students)
        val_num_correct = calculate_num_correct(curr_students)
        val_topic_rights = calculate_topic_rights(curr_students)
        val_topic_avgs = calculate_topic_averages(curr_students)

        curr_assumptions = {}
        for k in assumptions:
            for j in student_list:
                if k == j[get_keyword_value("id")]:
                    curr_assumptions[k] = assumptions[k]
        val_assumptions = {assumptions_key: curr_assumptions}

        result = {'overall_quiz': {'average': val_average['average'],
                                   'kr20': val_kr20['kr20'],
                                   'weighted_avg': val_weighted_avg['weighted_avg']},
                  'overall_items': {'diff_avg': val_diff_avg['diff_avg'],
                                    'idr_avg': val_idr_avg['idr_avg']},
                  'item_analysis': [],
                  'student_scores': []}

        for k in val_difficulty['difficulty']:
            result['item_analysis'].append({'item_id': k,
                                            'difficulty': val_difficulty['difficulty'][k],
                                            'idr': val_idr['idr'][k],
                                            'num_correct': val_num_correct['num_correct'][k]})

        for k in val_scores['scores']:
            result['student_scores'].append({'student': k,
                                             'score': val_scores['scores'][k],
                                             'weighted_score': val_weighted_s['weighted_scores'][k]})

        items = [val_excludes, val_assumptions,
                 val_topic_rights, val_topic_avgs]
        for item in items:
            result.update(item)

        group_analysis[i] = result

    return {service_key: group_analysis}
