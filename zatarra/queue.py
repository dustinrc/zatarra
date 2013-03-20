#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.queue
   ~~~~~~~~~~~~~

"""


import heapq
import time
import uuid


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

        if key is None:
            key = str(uuid.uuid4())

        entry = (priority, time.time(), item, key)
        self.entries[key] = entry
        heapq.heappush(self.heap, entry)

        return key

