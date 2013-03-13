#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests
   ~~~~~~~~~~~~~

"""


import unittest

import time


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        def _time_gen():
            epoch = 0.0
            while True:
                epoch += 0.000125
                yield epoch

        self._old_time = time.time
        _time = _time_gen()
        time.time = lambda: next(_time)

    def tearDown(self):
        time.time = self._old_time

