#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.queue
   ~~~~~~~~~~~~~

"""


import heapq
import time



PRIORITY = 0
REMOVED = '<REMOVED>'


class Queue(object):
    """
    """

    def __init__(self):
        self.heap = []
        self.entries = {}

    def put(self, item, priority=PRIORITY, key=None):
        """
        """

        entry = (priority, time.time(), item)
        self.entries[item] = entry
        heapq.heappush(self.heap, entry)

