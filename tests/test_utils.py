import common.utils as utils
from common.config import initialize_config, get_config, get_service_config

import tests.expecteds as exp


class TestUtils:
    data = None

    # This is called before the actual tests are called.
    # self.data is a class variable that can be used through out the class
    def setup(self):
        initialize_config(True)  # with default config
        self.data = {
            "exam":
                {
                    "name": "test1"
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
                    "group": ["2022"],
                    "id": "1234",
                    "first_name": "John",
                    "last_name": "Smith",
                    "email": "johnsmith@email.com",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "3", "response": 0},
                        {"item_id": "2", "response": 1},
                        {"item_id": "4", "response": 1},
                        {"item_id": "5", "response": 0},
                        {"item_id": "8", "response": 1}
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
                {"group": ["2024"],
                 "id": "1236",
                 "first_name": "Jake",
                 "last_name": "Jakey",
                 "email": "jakejakey@email.com",
                 "item_responses": [
                     {"item_id": "2", "response": 0},
                     {"item_id": "1", "response": 1},
                     {"item_id": "3", "response": 0},
                     {"item_id": "4", "response": 0},
                     {"item_id": "6", "response": 0},
                     {"item_id": "5", "response": 1},
                     {"item_id": "7", "response": 1}
                 ]
                 }
            ],
            "exclude_items": [],
            "exclude_students": []
        }

    # test getting std
    def test_get_std(self):
        expected = 0.816496580927726
        std = utils.get_score_std(self.data)

        assert std == expected

    # test getting item ids
    def test_get_item_ids(self):
        expected = ["1", "2", "3", "4", "5", "6", "7", "8"]
        item_ids = utils.get_item_ids(self.data)

        assert item_ids == expected

    # test sorting responses
    def test_get_sorted_responses(self):
        expected = [[1, 1, 0, 1, 0, 0, 0, 1],
                    [0, 1, 1, 1, 1, 1, 0, 0],
                    [1, 0, 0, 0, 1, 0, 1, 0]]

        responses = utils.get_sorted_responses(self.data)
        print(responses)

        assert expected == responses

    # test getting groups
    def test_get_group_list(self):
        expected = ["2022", "2024"]
        group_list = utils.get_group_list(self.data)

        assert group_list == expected

    # test sorting by groups
    def test_sort_students_by_group(self):
        expected = exp.sort_by_group
        by_group = utils.sort_students_by_group(self.data)

        assert by_group == expected

    # test getting student ids
    def test_get_student_ids(self):
        expected = ["1234", "1235", "1236"]
        stud_ids = utils.get_student_ids(self.data)

        assert stud_ids == expected

    # test getting student list
    def test_get_student_list(self):
        expected = [
            {"email": "johnsmith@email.com",
             "first_name": "John",
             "group": ["2022"],
             "id": "1234",
             "item_responses": [{"item_id": "1", "response": 1},
                                {"item_id": "3", "response": 0},
                                {"item_id": "2", "response": 1},
                                {"item_id": "4", "response": 1},
                                {"item_id": "5", "response": 0},
                                {"item_id": "8", "response": 1}],
             "last_name": "Smith"},
            {"email": "janesmath@email.com",
             "first_name": "Jane",
             "group": ["2022"],
             "id": "1235",
             "item_responses": [{"item_id": "1", "response": 0},
                                {"item_id": "2", "response": 1},
                                {"item_id": "3", "response": 1},
                                {"item_id": "4", "response": 1},
                                {"item_id": "5", "response": 1},
                                {"item_id": "6", "response": 1}],
             "last_name": "Smath"},
            {"email": "jakejakey@email.com",
             "first_name": "Jake",
             "group": ["2024"],
             "id": "1236",
             "item_responses": [{"item_id": "2", "response": 0},
                                {"item_id": "1", "response": 1},
                                {"item_id": "3", "response": 0},
                                {"item_id": "4", "response": 0},
                                {"item_id": "6", "response": 0},
                                {"item_id": "5", "response": 1},
                                {"item_id": "7", "response": 1}],
             "last_name": "Jakey"},
        ]
        stud_list = utils.get_student_list(self.data)

        assert stud_list == expected

    # test updating input
    def test_update_input(self):
        data = {
            "student_list": [
                {
                    "item_responses": [
                        {"response": 1},
                        {"response": 0},
                    ]
                },
                {
                    "item_responses": [
                        {"response": 1},
                        {"response": 0},
                    ]
                }]}

        expected = {
            "exam": {
                "name": "unknown",
                "scoring_method": "unknown"
                },
            "student_list": [
                {
                    "group": ["unknown"],
                    "id": "1",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0},
                    ]
                },
                {
                    "group": ["unknown"],
                    "id": "2",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0},
                    ]
                }]}
        updated = utils.update_input(data)

        assert updated == expected

    # test getting topics
    def test_get_topics(self):
        expected = [
            {"topic_hierarchy": ((0,
                                  "Biology"),
                                 (1,
                                  "Cell biology"),
                                 (2,
                                  "Cells"),
                                 (3,
                                  "Organelles"),
                                 (4,
                                  "Nucleus"),
                                 (5,
                                  "DNA")),
             "topic_ids": ["1"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "Biology"),
                                 (1,
                                  "Cell biology"),
                                 (2,
                                  "Cells"),
                                 (3,
                                  "Organelles"),
                                 (4,
                                  "Ribosomes")),
             "topic_ids": ["1"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "A"),
                                 (1,
                                  "B"),
                                 (2,
                                  "C"),
                                 (3,
                                  "D"),
                                 (4,
                                  "E"),
                                 (5,
                                  "f")),
             "topic_ids": ["2",
                           "5"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "A"),
                                 (1,
                                  "B"),
                                 (2,
                                  "C"),
                                 (3,
                                  "D"),
                                 (4,
                                  "e")),
             "topic_ids": ["2"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "G"),
                                 (1,
                                  "H"),
                                 (2,
                                  "unknown"),
                                 (3,
                                  "J"),
                                 (4,
                                  "K"),
                                 (5,
                                  "l")),
             "topic_ids": ["3"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "G"),
                                 (1,
                                  "H"),
                                 (2,
                                  "I"),
                                 (3,
                                  "J"),
                                 (4,
                                  "k")),
             "topic_ids": ["3"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "M"),
                                 (1,
                                  "N"),
                                 (2,
                                  "O"),
                                 (3,
                                  "P"),
                                 (4,
                                  "Q"),
                                 (5,
                                  "r")),
             "topic_ids": ["4"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "M"),
                                 (1,
                                  "N"),
                                 (2,
                                  "O"),
                                 (3,
                                  "P"),
                                 (4,
                                  "q")),
             "topic_ids": ["4",
                           "6"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "m"),
                                 (1,
                                  "n"),
                                 (2,
                                  "o"),
                                 (3,
                                  "p"),
                                 (4,
                                  "q")),
             "topic_ids": ["5"],
             "topic_rights": 0},
            {"topic_hierarchy": ((0,
                                  "a"),
                                 (1,
                                  "b"),
                                 (2,
                                  "c"),
                                 (3,
                                  "d"),
                                 (4,
                                  "e"),
                                 (5,
                                  "f")),
             "topic_ids": ["6"],
             "topic_rights": 0},
        ]
        topics = utils.get_item_topics(self.data)

        assert topics == expected

    # testing with item excludes
    def test_with_item_excludes(self):
        data = {
            "student_list": [
                {
                    "id": 1,
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0},
                        {"item_id": "3", "response": 1},
                        {"item_id": "4", "response": 0}
                    ]
                },
                {
                    "id": 2,
                    "item_responses": [
                        {"item_id": "1", "response": 1}
                    ]
                }
            ],
            "exclude_items": ["4"]
        }

        expected = ["1", "2", "3"]
        id_list = utils.get_item_ids(data)

        assert id_list == expected

    # testing without item excludes
    def test_without_item_excludes(self):
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
                    "id": 1,
                    "item_responses": [
                        {"item_id": 1, "response": 1}
                    ]
                }
            ]
        }

        expected = [1, 2]
        id_list = utils.get_item_ids(data)

        assert id_list == expected

    # testing with student excludes
    def test_with_student_excludes(self):
        data = {
            "student_list": [
                {
                    "id": "1",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0}
                    ]
                },
                {
                    "id": "2",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0}
                    ]
                },
                {
                    "id": "3",
                    "item_responses": [
                        {"item_id": "1", "response": 1},
                        {"item_id": "2", "response": 0}
                    ]
                }
            ],
            "exclude_students": ["1"]
        }

        expected = ["2", "3"]
        stud_ids = utils.get_student_ids(data)

        assert stud_ids == expected

    # testing without student excludes
    def test_without_student_excludes(self):
        data = {
            "student_list": [
                {
                    "id": 1,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0}
                    ]
                },
                {
                    "id": 2,
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0}
                    ]
                }
            ]
        }

        expected = [1, 2]
        stud_ids = utils.get_student_ids(data)

        assert stud_ids == expected

    # test getting scoring method
    def test_get_scoring_method(self):
        data = {
            "exam": {
                "scoring_method": "percentage"
            },
            "student_list": [
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1},
                        {"item_id": 2, "response": 0}
                    ]
                },
                {
                    "item_responses": [
                        {"item_id": 1, "response": 1}
                    ]
                }
            ]
        }

        expected = ("percentage", 1)
        method = utils.get_scoring_method(data)

        assert method == expected

    # test getting scoring with no students
    def test_get_scoring_method_no_students(self):
        data = {
            "exam": {
                "scoring_method": "percentage"
            }
        }

        expected = "Invalid data - Not enough students"
        method = utils.get_scoring_method(data)

        assert method == expected

    def test_get_config(self):
        expected = "Reliability Measures"
        assert get_config("application_org") == expected

        # read the secret
        expected = {
            "db_host": "",
            "db_user": "",
            "db_password": "",
            "db_name": "DB"
        }
        assert get_config("db_provider") == expected

        expected = "kr20"
        assert get_service_config(1) == expected

        expected = "Item discrimination"
        assert get_service_config(2, "name") == expected

        # not found
        expected = None
        assert get_service_config(5, "title") == expected