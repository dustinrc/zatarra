#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests.test_queue
   ~~~~~~~~~~~~~~~~~~~~~~~~

"""


import heapq

from zatarra.tests import BaseTestCase
from zatarra.queue import Queue, PRIORITY, REMOVED


class QueueDefaultsTest(BaseTestCase):

    def test_constants(self):
        """Constant defaults"""

        self.assertEqual(0, PRIORITY)
        self.assertEqual('<REMOVED>', REMOVED)

    def test_initialization(self):
        """Initialization defaults"""

        q = Queue()

        self.assertEqual([], q.heap)
        self.assertEqual({}, q.entries)


class QueuePutTest(BaseTestCase):

    def test_put(self):
        """Queue.put method"""

        q = Queue()
        key = q.put(1)

        expected_heap = [
            (0, 0.000125, 1, '00000000-0000-0000-0000-000000000001')
        ]
        expected_entries = {
            '00000000-0000-0000-0000-000000000001':
                (0, 0.000125, 1, '00000000-0000-0000-0000-000000000001')
        }
        self.assertEqual(expected_heap, q.heap)
        self.assertEqual(expected_entries, q.entries)
        self.assertEqual('00000000-0000-0000-0000-000000000001', key)

    def test_put_prioritory(self):
        """Queue.put method ordering w/ different priorities"""

        q = Queue()
        q.put(1)
        q.put(2, priority=-1)
        q.put(3, priority=-1)

        expected_smallest = [
            (-1, 0.00025, 2, '00000000-0000-0000-0000-000000000002'),
            (-1, 0.000375, 3, '00000000-0000-0000-0000-000000000003'),
            (0, 0.000125, 1, '00000000-0000-0000-0000-000000000001')
        ]
        actual_smallest = heapq.nsmallest(3, q.heap)

        self.assertEqual(expected_smallest, actual_smallest)

