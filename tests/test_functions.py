import json

from api.kr20 import calculate_kr20
from api.idr import calculate_idr, calculate_idr_average
from api.difficulty import calculate_difficulty, calculate_difficulty_average
from api.scores import calculate_scores, calculate_average
from api.analyze_test import analyze_test
from api.weighted_scores import calculate_weighted_scores, \
    calculate_weighted_average
from api.excludes import get_exclude_recos
from api.num_correct import calculate_num_correct
from api.assumptions import get_assumptions
from api.analyze_groups import analyze_groups
from api.topic_rights import calculate_topic_rights, calculate_topic_averages
from common.config import get_service_config, initialize_config
from common.sample import sample, sample_output

import tests.expecteds as exp


class TestFunctions:
    data = None

    # This is called before the actual tests are called.
    # self.data is a class variable that can be used through out the class
    def setup(self):
        initialize_config(True)  # with default config
        self.data = {
            "exam":
                {
                    "name": "test1",
                },
            "item_topics": [
                {
                    "item_id": "1",
                    "tags": [
                        {
                            "topic_tree": "Biology",
                            "topic_branch_hierarchy": {
                                "0": "Cell biology",
                                "1": "Cells",
                                "2": "Organelles",
                                "3": "Nucleus"
                            },
                            "topic_tagged": "DNA",
                            "scored": "Y"
                        },
                        {
                            "topic_tree": "Biology",
                            "topic_branch_hierarchy": {
                                "0": "Cell biology",
                                "1": "Cells",
                                "2": "Organelles"
                            },
                            "topic_tagged": "Ribosomes",
                            "scored": "Y"
                        }
                    ]
                },
                {
                    "item_id": "2",
                    "tags": [
                        {
                            "topic_tree": "A",
                            "topic_branch_hierarchy": {
                                "0": "B",
                                "1": "C",
                                "2": "D",
                                "3": "E"
                            },
                            "topic_tagged": "f",
                            "scored": "Y"
                        },
                        {
                            "topic_tree": "A",
                            "topic_branch_hierarchy": {
                                "0": "B",
                                "1": "C",
                                "2": "D"
                            },
                            "topic_tagged": "e",
                            "scored": "Y"
                        }
                    ]
                },
                {
                    "item_id": "3",
                    "tags": [
                        {
                            "topic_tree": "G",
                            "topic_branch_hierarchy": {
                                "0": "H",
                                "1": "I",
                                "2": "J",
                                "3": "K"
                            },
                            "topic_tagged": "l",
                            "scored": "Y"
                        },
                        {
                            "topic_tree": "G",
                            "topic_branch_hierarchy": {
                                "0": "H",
                                "1": "I",
                                "2": "J"
                            },
                            "topic_tagged": "k",
                            "scored": "Y"
                        }
                    ]
                },
                {
                    "item_id": "4",
                    "tags": [
                        {
                            "topic_tree": "M",
                            "topic_branch_hierarchy": {
                                "0": "N",
                                "1": "O",
                                "2": "P",
                                "3": "Q"
                            },
                            "topic_tagged": "r",
                            "scored": "Y"
                        },
                        {
                            "topic_tree": "M",
                            "topic_branch_hierarchy": {
                                "0": "N",
                                "1": "O",
                                "2": "P",
                            },
                            "topic_tagged": "q",
                            "scored": "Y"
                        }
                    ]
                },
                {
                    "item_id": "5",
                    "tags": [
                        {
                            "topic_tree": "A",
                            "topic_branch_hierarchy": {
                                "0": "B",
                                "1": "C",
                                "2": "D",
                                "3": "E"
                            },
                            "topic_tagged": "f",
                            "scored": "Y"
                        },
                        {
                            "topic_tree": "m",
                            "topic_branch_hierarchy": {
                                "0": "n",
                                "1": "o",
                                "2": "p",
                            },
                            "topic_tagged": "q",
                            "scored": "Y"
                        }
                    ]
                },
                {
                    "item_id": "6",
                    "tags": [
                        {
                            "topic_tree": "a",
                            "topic_branch_hierarchy": {
                                "0": "b",
                                "1": "c",
                                "2": "d",
                                "3": "e"
                            },
                            "topic_tagged": "f",
                            "scored": "Y"
                        },
                        {
                            "topic_tree": "M",
                            "topic_branch_hierarchy": {
                                "0": "N",
                                "1": "O",
                                "2": "P",
                            },
                            "topic_tagged": "q",
                            "scored": "Y"
                        }
                    ]
                },
            ],
            "student_list": [
                {
                    "group": ["2022", "class 1"],
                    "id": "1234",
                    "first_name": "John",
                    "last_name": "Smith",
                    "email": "johnsmith@email.com",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0},
                        {"item_id": "3", "response": 1},
                        {"item_id": "4", "response": 1},
                        {"item_id": "5", "response": 0},
                        {"item_id": "6", "response": 1}
                    ]
                },
                {"group": ["2022"],
                 "id": "1235",
                 "first_name": "Jane",
                 "last_name": "Smath",
                 "email": "janesmath@email.com",
                 "item_responses": [
                     {"item_id": "1", "response": 0},
                     {"item_id": "2", "response": 1},
                     {"item_id": "3", "response": 1},
                     {"item_id": "4", "response": 1},
                     {"item_id": "5", "response": 1},
                     {"item_id": "6", "response": 1}
                 ]
                 },
                {"group": ["2024", "class 1"],
                 "id": "1236",
                 "first_name": "Jake",
                 "last_name": "Jakey",
                 "email": "jakejakey@email.com",
                 "item_responses": [
                     {"item_id": "1", "response": 0},
                     {"item_id": "2", "response": 1},
                     {"item_id": "3", "response": 0},
                     {"item_id": "4", "response": 0},
                     {"item_id": "5", "response": 0},
                     {"item_id": "6", "response": 1},
                     {"item_id": "7", "response": 1}
                 ]
                 }
            ],
            "exclude_items": [],
            "exclude_students": []
        }

    # testing analyze_test with sample data
    def test_sample_analyze(self):
        analysis = analyze_test(sample)
        assert json.dumps(analysis) == json.dumps(sample_output[0])

        sample["exclude_items"] = [2, 6, 9, 12, 15, 16, 17, 18]
        analysis2 = analyze_test(sample)
        assert json.dumps(analysis2) == json.dumps(sample_output[1])

    # testing analyze_test
    def test_analyze(self):
        expected = exp.test_analysis

        analysis = json.dumps(analyze_test(self.data))
        assert json.loads(analysis) == expected

    # testing the kr_20
    def test_kr20(self):
        expected = -1.167
        kr20 = calculate_kr20(self.data)[get_service_config(1)]

        assert kr20 == expected

    # testing the idr
    def test_idr(self):
        expected = {"1": 0.0, "2": 0.0, "3": 0.082, "4": 0.082, "5": 0.082,
                    "6": 0.0, "7": -0.082}
        idr = calculate_idr(self.data)["idr"]

        assert idr == expected

    # testing the difficulty
    def test_difficulty(self):
        expected = {"1": 0.667, "2": 0.333, "3": 0.333, "4": 0.333, "5": 0.667,
                    "6": 0.0, "7": 0.667}
        difficulty = calculate_difficulty(self.data)["difficulty"]
        assert difficulty == expected

    # testing the scores
    def test_scores(self):
        expected = {"1234": 0.571, "1235": 0.714, "1236": 0.429}
        scores = calculate_scores(self.data)["scores"]

        assert scores == expected

    # testing the average
    def test_average(self):
        expected = 0.571
        average = calculate_average(self.data)["average"]

        assert average == expected

    # testing the weighted scores
    def test_weighted_scores(self):
        expected = {"1234": 0.444, "1235": 0.555, "1236": 0.333}
        weighted_scores = calculate_weighted_scores(self.data)[
            "weighted_scores"]

        assert weighted_scores == expected

    # testing the weighted average
    def test_weighted_avg(self):
        expected = 0.444
        weighted_average = calculate_weighted_average(self.data)[
            "weighted_avg"]

        assert weighted_average == expected

    # testing the get excludes
    def test_get_exclude_recos(self):
        expected = ["7"]
        excludes = get_exclude_recos(self.data)["exclude"]

        assert excludes == expected

    # testing the avg difficulty
    def test_difficulty_avg(self):
        expected = 0.429
        diff_avg = calculate_difficulty_average(self.data)["diff_avg"]

        assert diff_avg == expected

    # testing the avg idr
    def test_idr_avg(self):
        expected = 0.023
        idr_avg = calculate_idr_average(self.data)["idr_avg"]

        assert idr_avg == expected

    # testing the num correct
    def test_num_correct(self):
        expected = {"1": 1, "2": 2, "3": 2, "4": 2, "5": 1, "6": 3, "7": 1}
        num_correct = calculate_num_correct(self.data)["num_correct"]

        assert num_correct == expected

    # testing the assumptions
    def test_assumptions(self):
        expected = {"1234": {"assumed": ["7"]}, "1235": {"assumed": ["7"]}}
        assumption = get_assumptions(self.data)["assumptions"]

        assert assumption == expected

    # testing analysis by group
    def test_group_analysis(self):
        expected = exp.group_analysis
        analysis = json.dumps(analyze_groups(self.data)["group_analysis"])

        assert json.loads(analysis) == expected

    # testing topic scores
    def test_topic_score(self):
        expected = exp.topic_score
        topic_rights = calculate_topic_rights(self.data)["topic_rights"]

        assert topic_rights == expected

    # testing topic averages
    def test_topic_avgs(self):
        expected = exp.topic_avgs
        topic_rights = calculate_topic_averages(self.data)["topic_avgs"]

        assert topic_rights == expected
