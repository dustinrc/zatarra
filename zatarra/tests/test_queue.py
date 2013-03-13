#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests.test_queue
   ~~~~~~~~~~~~~~~~~~~~~~~~

"""


import unittest

import os
import time

from zatarra.queue import Queue, PRIORITY, REMOVED


class QueueDefaultsTest(unittest.TestCase):

    def test_constants(self):
        """Constant defaults"""

        self.assertEqual(0, PRIORITY)
        self.assertEqual('<REMOVED>', REMOVED)

    def test_initialization(self):
        """Initialization defaults"""

        q = Queue()

        self.assertEqual([], q.heap)
        self.assertEqual({}, q.entries)


class QueuePutTest(unittest.TestCase):

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

    def test_put(self):
        """Queue.put method"""

        q = Queue()
        q.put(1)

        self.assertEqual([(0, 0.000125, 1)], q.heap)
        self.assertEqual({1: (0, 0.000125, 1)}, q.entries)

