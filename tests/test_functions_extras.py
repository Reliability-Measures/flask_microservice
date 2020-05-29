from api.idr import calculate_idr
from api.analyze_test import analyze_test
from api.analyze_groups import analyze_groups
from api.scores import calculate_average, calculate_scores
from api.weighted_scores import calculate_weighted_average, calculate_weighted_scores

import tests.expecteds as exp


class TestFunctions:

    # testing with no group
    def test_no_group(self):
        data = {
            "student_list": [
                {
                    "id": 1,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0},
                    ]
                },
                { 
                    "id": 2,
                    "item_responses": [
                        {"item_id": 1, "response": 0},
                        {"item_id": 2, "response": 1},
                    ]
                },
                { 
                    "id": 3,
                    "item_responses": [
                        {"item_id": 1, "response": 0},
                        {"item_id": 2, "response": 1},
                    ]
                }
            ]
        }

        expected = "No groups were found, or all students are in the same group"
        analysis = analyze_groups(data)["group_analysis"]

        assert analysis == expected

    # testing item exclude calcs
    def test_item_excludes_difference(self):
        data_1 = {
            "student_list": [
                {
                    "id": 1,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 0}
                    ]
                },
                { 
                    "id": 2,
                    "item_responses": [
                        {"item_id": 1, "response": 0},
                        {"item_id": 2, "response": 1},
                        {"item_id": 3, "response": 0},
                        {"item_id": 4, "response": 1}
                    ]
                },
                { 
                    "id": 3,
                    "item_responses": [
                        {"item_id": 1, "response": 0},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 1}
                    ]
                },
                { 
                    "id": 4,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 1},
                        {"item_id": 3, "response": 0},
                        {"item_id": 4, "response": 0}
                    ]
                }
            ],
            "exclude_items": [4]
        }
        data_2 = {
            "student_list": [
                {
                    "id": 1,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 0}
                    ]
                },
                { 
                    "id": 2,
                    "item_responses": [
                        {"item_id": 1, "response": 0},
                        {"item_id": 2, "response": 1},
                        {"item_id": 3, "response": 0},
                        {"item_id": 4, "response": 1}
                    ]
                },
                { 
                    "id": 3,
                    "item_responses": [
                        {"item_id": 1, "response": 0},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 1}
                    ]
                },
                { 
                    "id": 4,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 1},
                        {"item_id": 3, "response": 0},
                        {"item_id": 4, "response": 0}
                    ]
                }
            ],
            "exclude_items": [1,3]
        }

        idr_1 = calculate_idr(data_1)
        idr_2 = calculate_idr(data_2)

        assert idr_1 != idr_2

    # test analysis with no group, student id, or item id
    def test_optional_inputs(self):
        data = {
            "student_list": [
                {
                    "item_responses": [
                        {"response": 1},
                        {"response": 0},
                        {"response": 0}
                    ]
                },
                { 
                    "item_responses": [
                        {"response": 0},
                        {"response": 1},
                        {"response": 1}
                    ]
                },
                { 
                    "item_responses": [
                        {"response": 0},
                        {"response": 1},
                    ]
                }
            ]
        }

        expected = {'analysis': {'assumptions': {'3': {'assumed': ['3']}}, 'exclude': ['1'], 'group_analysis': 'No groups were found, or all students are in the same group', 'item_analysis': [{'difficulty': 0.667, 'idr': -0.037, 'item_id': '1', 'num_correct': 1},
                  {'difficulty': 0.333, 'idr': 0.037, 'item_id': '2', 'num_correct': 2}, {'difficulty': 0.667, 'idr': 0.074, 'item_id': '3', 'num_correct': 1}], 'overall_items': {'diff_avg': 0.556, 'idr_avg': 0.025},    
          'overall_quiz': {'average': 0.444, 'kr20': -3.0, 'weighted_avg': 0.4}, 'student_scores': [{'score': 0.333,  'student': '1',  'weighted_score': 0.4}, {'score': 0.667,  'student': '2',  'weighted_score': 0.6},      
                           {'score': 0.333,  'student': '3',  'weighted_score': 0.2}], 'topic_avgs': 'No topics were found', 'topic_rights': 'No topics were found'}}
        analysis = analyze_test(data)

        assert analysis == expected

    # Test with empty json
    def test_empty_json(self):
        data = {}

        expected = {"analysis": "Invalid data - Not enough students"}
        analysis = analyze_test(data)

        assert analysis == expected

    # Test with one student
    def test_one_student(self):
        data = {"student_list": [{}]}

        expected = {"analysis": "Invalid data - Not enough students"}
        analysis = analyze_test(data)

        assert analysis == expected

    # test with no items
    def test_no_items(self):
        data = {"student_list": [
            {
                "item_responses": []
            },
            {
                "item_responses": []
            },
            {
                "item_responses": []
            }
        ]}

        expected = {"analysis": "Invalid data - Not enough items"}
        analysis = analyze_test(data)

        assert analysis == expected

    # test with one item
    def test_one_item(self):
        data = {"student_list": [
            {
                "item_responses": [{}]
            },
            {
                "item_responses": []
            },
            {
                "item_responses": []
            }
        ]}

        expected = {"analysis": "Invalid data - Not enough items"}
        analysis = analyze_test(data)
        print(analysis)

        assert analysis == expected

    def test_missing_data_1(self):
        data = {
            "student_list": [
                {
                    "item_responses": [
                        {"response": 1},
                        {"response": 0}
                    ]
                },
                { 
                    "item_responses": [
                        {"response": 0}
                    ]
                },
                { 
                }
            ]
        }

        expected = {'analysis': {'assumptions': {'2': {'assumed': ['2']}, '3': {'assumed': ['1', '2']}}, 'exclude': 'Invalid data - No mean', 'group_analysis': 'No groups were found, or all students are in '   'the same group', 'item_analysis': [{'difficulty': 0.667,    'idr': 'Invalid data - No mean', 'item_id': '1',    'num_correct': 1},   {'difficulty': 1.0,    'idr': 'Invalid data - No mean', 'item_id': '2',    'num_correct': 0}], 'overall_items': {'diff_avg': 0.834,   'idr_avg': 'Invalid data - No mean'}, 'overall_quiz': {'average': 0.167,  'kr20': -0.0,  'weighted_avg': 0.133}, 'student_scores': [{'score': 0.5,     'student': '1', 'weighted_score': 0.4},    {'score': 0.0,     'student': '2',     'weighted_score': 0.0},    {'score': 0.0,     'student': '3',     'weighted_score': 0.0}], 'topic_avgs': 'No topics were found', 'topic_rights': 'No topics were found'}}
        analysis = analyze_test(data)

        assert analysis == expected

    def test_missing_data_2(self):
        data = {
            "item_topics":[
                {
                    "item_id":"1",
                    "tags":[
                        {
                        "topic_tagged":"DNA",
                        "scored":"Y"
                        },
                        {
                        "topic_tree":"Biology",
                        "topic_branch_hierarchy":{
                            "0":"Cell biology",
                            "1":"Cells",
                            "2":"Organelles"
                        },
                        "topic_tagged":"Ribosomes",
                        "scored":"Y"
                        }
                    ]
                },
                {
                    "tags":[
                        {
                        "topic_tree":"A",
                        "topic_branch_hierarchy":{
                            "0":"B",
                            "1":"C",
                            "2":"D",
                            "3":"E"
                        },
                        "topic_tagged":"f",
                        "scored":"Y"
                        },
                        {
                        "topic_tree":"m",
                        "topic_branch_hierarchy":{
                        }
                        }
                    ]
                },
                {
                    "item_id":"6",
                },
            ],
            "student_list": [
                { 
                  "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0},
                        {"item_id": "3", "response": 1},
                        {"item_id": "4", "response": 1},
                        {"item_id": "5", "response": 0},
                        {"item_id": "6", "response": 1}
                    ]
                },
                { "group": ["2022"],
                  "email": "janesmath@email.com",
                  "item_responses": [
                        {"item_id": "4", "response": 1},
                        {"item_id": "5", "response": 1},
                        {"item_id": "6", "response": 1}
                    ]
                },
                { "group": ["2024"],
                  "item_responses": [
                        {"item_id": "1", "response": 0},
                        {"item_id": "2", "response": 1},
                        {"item_id": "3", "response": 0},
                        {"item_id": "4", "response": 0}
                    ]
                }
            ]
        }

        expected = exp.missing_data_2
        analysis = analyze_test(data)

        assert analysis == expected

    def test_percentage_method(self):
        data = {
            "exam": {
                "scoring_method": "percentage"
            },
            "student_list": [
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 1}
                    ]
                },
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1}
                    ]
                }
            ]
        }

        expected = ({"scores": {"1": 75.0, "2": 25.0}}, {"average": 50.0}, 
                    {"weighted_scores": {"1": 50.0, "2": 0.0}}, {"weighted_avg": 25.0})
        scoring = (calculate_scores(data), calculate_average(data), 
                   calculate_weighted_scores(data), calculate_weighted_average(data))

        assert scoring == expected

    def test_absolute_method(self):
        data = {
            "exam": {
                "scoring_method": "absolute"
            },
            "student_list": [
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 1}
                    ]
                },
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1}
                    ]
                }
            ]
        }

        expected = ({"scores": {"1": 3.0, "2": 1.0}}, {"average": 2.0}, 
                    {"weighted_scores": {"1": 2.0, "2": 0.0}}, {"weighted_avg": 1.0})
        scoring = (calculate_scores(data), calculate_average(data), 
                   calculate_weighted_scores(data), calculate_weighted_average(data))

        assert scoring == expected

    def test_scaled_method(self):
        data = {
            "exam": {
                "scoring_method": "scaled",
                "scaled_factor": .79
            },
            "student_list": [
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0},
                        {"item_id": 3, "response": 1},
                        {"item_id": 4, "response": 1}
                    ]
                },
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1}
                    ]
                }
            ]
        }

        expected = ({"scores": {"1": 0.593, "2": 0.198}}, {"average": 0.395}, 
                    {"weighted_scores": {"1": 0.395, "2": 0.0}}, {"weighted_avg": 0.198})
        scoring = (calculate_scores(data), calculate_average(data), 
                   calculate_weighted_scores(data), calculate_weighted_average(data))

        assert scoring == expected