import os.path
import unittest

class TestCapV2(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestCapV2, self).__init__(*args, **kwargs)
        self.logs = []

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_naive_case(self):
        expected = 3
        result = 3
        self.logs.append((expected, result))
        self.assertEqual(result, expected)
