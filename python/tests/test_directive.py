import unittest

import directive as dtv


class TestLoad(unittest.TestCase):
    def test_load_prelude(self):
        status = dtv.eval_directive("load", ["prelude"])

        self.assertIsNone(status["error"])

        program = status["user_data"]

        self.assertEqual(len(program), 13)
