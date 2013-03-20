#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests
   ~~~~~~~~~~~~~

"""


import unittest

import time
import uuid


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

        def _uuid_gen():
            num = 0
            while True:
                num += 1
                yield uuid.UUID('00000000-0000-0000-0000-{:012x}'.format(num))

        self._old_uuid4 = uuid.uuid4
        _uuid4 = _uuid_gen()
        uuid.uuid4 = lambda: next(_uuid4)

    def tearDown(self):
        time.time = self._old_time
        uuid.uuid4 = self._old_uuid4

