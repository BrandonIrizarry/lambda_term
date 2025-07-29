import unittest
import pprint
from main import *


class TestParseTerm(unittest.TestCase):
    def test(self):
        raw_term = "   ((\\input.\\func.(  func input  ) \\first.\\second.first) \\sole.sole)"
        tokens = tokenize(raw_term)

        parsed, num_tokens = parse_term(tokens, 0, [])

        self.assertEqual(parsed, {'kind': 'application',
                                  'left': {'kind': 'application',
                                           'left': {'body': {'body': {'kind': 'application',
                                                                      'left': {'index': 0, 'kind': 'name'},
                                                                      'right': {'index': 1, 'kind': 'name'}},
                                                             'kind': 'abstraction'},
                                                    'kind': 'abstraction'},
                                           'right': {'body': {'body': {'index': 1, 'kind': 'name'},
                                                              'kind': 'abstraction'},
                                                     'kind': 'abstraction'}},
                                  'right': {'body': {'index': 0, 'kind': 'name'}, 'kind': 'abstraction'}})

        self.assertEqual(num_tokens, 25)
