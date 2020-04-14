from weighted_scores import calculate_weighted_scores
from config import get_service_config


def calculate_weighted_average(param):
    service_key = get_service_config(8)
    weighted_scores = list(list(calculate_weighted_scores(param).values())[0].values())
    numStudents = len(weighted_scores)
    weighted_average = sum(weighted_scores) / numStudents
        
    return {service_key: round(weighted_average, 1)}
