from providers.cloud_handler import get_config_file
from common.subjects import subjects

global config
# JSON object for literals and constants
# will be hosted in some cloud storage
# all keys are lower case, Use underscore for longer keys

# need to read from env
cloud_provider = {
    "cloud_host": "dropbox",
    "cloud_config_file": "config.json",
    "cloud_subjects_file": "subjects.json",
    "cloud_rm_file": "rm_secrets.json",
    "cloud_access_key": "vDuiM-56ZzsAAAAAAAAHJGw5MRrhkkeJZ0AJhft11_SCePhuuP2XCVGY3pMGvLBn",
}

secret_config = {
    "application_client_id": "xxxxx."
                             "apps.googleusercontent.com",

    "db_provider": {
        "db_host": "",
        "db_user": "",
        "db_password": "",
        "db_name": "DB"
    },
    "db_provider_cloud": {
        "db_host": "",
        "db_user": "",
        "db_password": "",
        "db_name": "DB"
    },
}

# default
default_config = {
    "application_id": "rm_01",
    "application_version": "0.4.2",
    "application_name": "Reliability Measures microservices",
    "application_org": "Reliability Measures",
    "application_email": "info@reliabilitymeasures.com",
    "application_short_name": "rm_microservices",
    "service_url": "http://api.reliabilitymeasures.com/",
    "service2_url": "http://api2.reliabilitymeasures.com/",
    "test_url": "http://localhost:5000/",
    "login_method": "login/",
    "classroom_method": "classroom/",
    "sample_method": "sample/",
    "quiz_method": "quiz/",
    "item": "item/",
    "create_item": "create_item/",
    "edit_item": "edit_item/",
    "get_items": "get_items/",
    "create_form": "create_form/",
    "quiz_account": "quiz_account/",
    "keywords": {
            "exam": "exam",
            "name": "name",
            "scoring_method": "scoring_method",
            "absolute": "absolute",
            "percentage": "percentage",
            "scaled": "scaled",
            "scaled_factor": "scaled_factor",
            "exclude_students": "exclude_students",
            "exclude_items": "exclude_items",

            "item_responses": "item_responses",
            "student_list": "student_list",
            "item_id": "item_id",
            "response": "response",
            "id": "id",
            "group": "group",

            "item_topics": "item_topics",
            "tags": "tags",
            "scored": "scored",
            "topic_branch_hierarchy": "topic_branch_hierarchy",
            "topic_tagged": "topic_tagged",
            "topic_tree": "topic_tree",
            "topic_ids": "topic_ids",
            "topic_hierarchy": "topic_hierarchy",
            "topic_rights": "topic_rights",

            "exclude_threshold_1": 0.09,
            "exclude_threshold_2": 0,
            "exclude_length_1": 0.5,
            "exclude_length_2": 0.8,
            "unknown": "unknown",

            "bad_data": "Invalid data - Not enough students",
            "bad_num_items": "Invalid data - Not enough items",
            "bad_std": "Invalid data - No Std. Dev.",
            "bad_mean": "Invalid data - No mean",
            "no_group": "No groups were found, or all students are in the same group",
            "no_assumptions": "No student response assumptions were made",
            "no_topics": "No topics were found",
            "no_students": "No student information was found",
            "no_responses": "No student responses were found",
            "assumed": "assumed",
            "dupes": "duplicates"
    },  
    "services": [
        # use the shot_name key for service path and in response key.
        # Must follow Python/JS variable rules
        {"id": 0},  # left  empty on purpose
        {
            "id": 1,
            "name": "kr20",
            "short_name": "kr20",
            "description": "KR20 value",
            "type": "float"
        },
        {
            "id": 2,
            "name": "Item discrimination",
            "short_name": "idr",
            "description": "Item discrimination, "
                           "Point-Biserial correlation coefficient",
            "type": "list of floats"
        },
        {
            "id": 3,
            "name": "Item difficulty",
            "short_name": "difficulty",
            "description": "Item difficulty",
            "type": "list of floats"
        },
        {
            "id": 4,
            "name": "scores",
            "short_name": "scores",
            "description": "Test scores",
            "type": "list of floats"
        },
        {
            "id": 5,
            "name": "average",
            "short_name": "average",
            "description": "Student Average",
            "type": "list of floats"
        },
        {
            "id": 6,
            "name": "Test Analysis",
            "short_name": "analysis",
            "api_method": "analyzeTest/",
            "description": "The whole test analysis with all results",
            "type": "list of items"
        },
        {
            "id": 7,
            "name": "Weighted Scores",
            "short_name": "weighted_scores",
            "description": "Weighted test scores",
            "type": "list of floats"
        },
        {
            "id": 8,
            "name": "Weighted Average",
            "short_name": "weighted_avg",
            "description": "Weighted Average of Weighted test scores",
            "type": "float"
        },
        {
            "id": 9,
            "name": "exclude_items",
            "short_name": "exclude",
            "description": "Items to exclude based on idr",
            "type": "list of item ids"
        },
        {
            "id": 10,
            "name": "difficulty_average",
            "short_name": "diff_avg",
            "description": "The average difficulty",
            "type": "float"
        },
        {
            "id": 11,
            "name": "discrimination_average",
            "short_name": "idr_avg",
            "description": "The average item discrimination",
            "type": "float"
        },
        {
            "id": 12,
            "name": "number_of_correct_responses",
            "short_name": "num_correct",
            "description": "The absolute number of an item\'s "
                           "correct responses",
            "type": "list of ints"
        },
        {
            "id": 13,
            "name": "student_response_assumptions",
            "short_name": "assumptions",
            "description": "The assumption of the score 0 for items that "
                           "the student does not have a response for",
            "type": "dictionary of item ids"
        },
        {
            "id": 14,
            "name": "analysis_by_group",
            "short_name": "group_analysis",
            "description": "Analysis of students\' responses based on "
                           "their group",
            "type": "dictionary of exam analyses"
        },
        {
            "id": 15,
            "name": "topic_right_responses",
            "short_name": "topic_rights",
            "description": "Each students\' number of right responses in each topic",
            "type": "dictionary of topic rights"
        },
        {
            "id": 16,
            "name": "topic_right_averages",
            "short_name": "topic_avgs",
            "description": "The average number of right responses in each topic",
            "type": "dictionary of topic right averages"
        }
    ] 
}


class Config:
    config = None
    secrets = None
    subjects = None

    def __init__(self):
        self.config = default_config
        self.secrets = secret_config
        self.subjects = subjects

    def get_keyword_value(self, key):
        return self.config["keywords"][key]

    def get_service_config(self, service_id, field="short_name"):
        service = self.config["services"][service_id]
        return service.get(field)

    def get_config(self, config_key, sub_key=None):
        if sub_key:
            value = self.config.get(config_key, {}).get(sub_key)
        else:
            value = self.config.get(config_key) or self.secrets.get(config_key)
        return value

    def get_subject(self, subject_key, sub_key=None):
        if sub_key:
            value = self.subjects["subject_list"].get(subject_key, {}).\
                get(sub_key)
        else:
            value = self.subjects["subject_list"].get(subject_key)
        return value

    def get_config_from_cloud(self):
        try:
            self.config = get_config_file(cloud_provider)
            self.subjects = get_config_file(cloud_provider,
                                            "cloud_subjects_file")
            self.secrets = get_config_file(cloud_provider, "cloud_rm_file")
        except Exception as exc:
            print("Config Exception!")


def initialize_config(default=False):
    global config
    config = Config()
    if not default:
        config.get_config_from_cloud()


def get_config(config_key, sub_key=None):
    return config.get_config(config_key, sub_key)


def get_service_config(service_id, field="short_name"):
    return config.get_service_config(service_id, field)


def get_keyword_value(key):
    return config.get_keyword_value(key)


def get_subjects():
    return config.subjects.get("subject_list")