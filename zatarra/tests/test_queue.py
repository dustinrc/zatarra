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
        """Queue constant defaults"""

        self.assertEqual(0, PRIORITY)
        self.assertEqual('<REMOVED>', REMOVED)

    def test_initialization(self):
        """Queue initialization defaults"""

        q = Queue()

        self.assertEqual([], q.heap)
        self.assertEqual({}, q.entries)


class QueuePutTest(BaseTestCase):

    def test_put(self):
        """Queue.put method"""

        q = Queue()
        key = q.put(1)

        expected_heap = [
            [0, 0.000125, 1, '00000000-0000-0000-0000-000000000001']
        ]
        expected_entries = {
            '00000000-0000-0000-0000-000000000001':
                [0, 0.000125, 1, '00000000-0000-0000-0000-000000000001']
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
            [-1, 0.00025, 2, '00000000-0000-0000-0000-000000000002'],
            [-1, 0.000375, 3, '00000000-0000-0000-0000-000000000003'],
            [0, 0.000125, 1, '00000000-0000-0000-0000-000000000001']
        ]
        actual_smallest = heapq.nsmallest(3, q.heap)

        self.assertEqual(expected_smallest, actual_smallest)

    def test_put_overwrite(self):
        """Queue.put method overwriting existing item"""

        q = Queue()
        key1 = q.put(1)
        key2 = q.put(2, priority=2, key=key1)

        expected_heap = [
            [0, 0.000125, REMOVED, '00000000-0000-0000-0000-000000000001'],
            [2, 0.00025, 2, '00000000-0000-0000-0000-000000000001']
        ]
        expected_entries = {
            '00000000-0000-0000-0000-000000000001':
                [2, 0.00025, 2, '00000000-0000-0000-0000-000000000001']
        }
        self.assertEqual(expected_heap, q.heap)
        self.assertEqual(expected_entries, q.entries)
        self.assertEqual(key1, key2)


class QueueGetTest(BaseTestCase):

    def test_get(self):
        """Queue.get method"""

        q = Queue()
        q.put('Moe')

        expected_get = ('Moe', '00000000-0000-0000-0000-000000000001')
        actual_get = q.get()

        self.assertEqual(expected_get, actual_get)
        self.assertEqual([], q.heap)
        self.assertEqual({}, q.entries)


class QueueHousekeepingTest(BaseTestCase):

    def test_clean(self):
        """Queue.clean method"""

        q = Queue()
        key1 = q.put(1)
        q.put(2)
        key3 = q.put(3)
        q.remove(key1)
        q.remove(key3)
        q.clean()

        expected_heap = [
            [0, 0.00025, 2, '00000000-0000-0000-0000-000000000002']
        ]

        self.assertEqual(expected_heap, q.heap)

    def test_remove(self):
        """Queue.remove method"""

        q = Queue()
        key = q.put(1)
        q.remove(key)

        expected_heap = [
            [0, 0.000125, REMOVED, '00000000-0000-0000-0000-000000000001']
        ]
        expected_entries = {}

        self.assertEqual(expected_heap, q.heap)
        self.assertEqual(expected_entries, q.entries)

