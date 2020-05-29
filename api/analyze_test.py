from common.config import get_service_config
from common.utils import update_input, get_error
from api.kr20 import calculate_kr20
from api.idr import calculate_idr, calculate_idr_average
from api.difficulty import calculate_difficulty, calculate_difficulty_average
from api.scores import calculate_scores, calculate_average
from api.weighted_scores import calculate_weighted_scores, calculate_weighted_average
from api.excludes import get_exclude_recos
from api.num_correct import calculate_num_correct
from api.assumptions import get_assumptions
from api.analyze_groups import analyze_groups
from api.topic_rights import calculate_topic_rights, calculate_topic_averages


def analyze_test(param):
    """
    A function to get an exam's analysis:
    It calls every service used to analyze
    an exam and then returns the analysis.

    :param: a json in the Reliabilty Measures
            standard json format
    :return: a dictionary of dictionaries:
             a dictionary with the results
             of the services as values
    """
    service_key = get_service_config(6)
    catch_error = get_error(param)
    if catch_error[0]:
        return {service_key: catch_error[1]}
    inp = update_input(param)
    # use microservice calls here when all are hosted
    val_kr20 = calculate_kr20(inp)
    val_idr = calculate_idr(inp)
    val_difficulty = calculate_difficulty(inp)
    val_scores = calculate_scores(inp)
    val_average = calculate_average(inp)
    val_weighted_s = calculate_weighted_scores(inp)
    val_weighted_avg = calculate_weighted_average(inp)
    val_excludes = get_exclude_recos(inp)
    val_diff_avg = calculate_difficulty_average(inp)
    val_idr_avg = calculate_idr_average(inp)
    val_num_correct = calculate_num_correct(inp)
    val_assumptions = get_assumptions(inp)
    val_topic_rights = calculate_topic_rights(inp)
    val_topic_avgs = calculate_topic_averages(inp)
    val_group_analysis = analyze_groups(inp)

    # join all results
    result = {'overall_quiz': {'average': val_average['average'],
                               'kr20': val_kr20['kr20'],
                               'weighted_avg': val_weighted_avg['weighted_avg']},
              'overall_items': {'diff_avg': val_diff_avg['diff_avg'],
                                'idr_avg': val_idr_avg['idr_avg']},
              'item_analysis': [],
              'student_scores': []}

    for i in val_difficulty['difficulty']:
        result['item_analysis'].append({'item_id': i,
                                        'difficulty': val_difficulty['difficulty'][i],
                                        'idr': val_idr['idr'][i],
                                        'num_correct': val_num_correct['num_correct'][i]})

    for i in val_scores['scores']:
        result['student_scores'].append({'student': i,
                                         'score': val_scores['scores'][i],
                                         'weighted_score': val_weighted_s['weighted_scores'][i]})

    items = [val_excludes, val_assumptions, val_topic_rights,
             val_group_analysis, val_topic_avgs]
    for item in items:
        result.update(item)

    return {service_key: result}


if __name__ == '__main__':
    from common.sample import sample
    from common.config import initialize_config
    from quiz.quiz_queries import decimal_default
    import json

    initialize_config()

    analysis = analyze_test(sample)
    print(json.dumps(analysis, indent=4,
                     default=decimal_default))
    #
    # sample["exclude_items"] = [2, 6, 9, 12, 15, 16, 17, 18]
    #
    # analysis = analyze_test(sample)
    #
    # print(json.dumps(analysis))
    