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

        if key in self.entries:
            self.remove(key)

        entry = [priority, time.time(), item, key]
        self.entries[key] = entry
        heapq.heappush(self.heap, entry)

        return key

    def get(self):
        """
        """

        priority, epoch_time, item, key = heapq.heappop(self.heap)

        while key == REMOVED:
            priority, epoch_time, item, key = heapq.heappop(self.heap)

        del self.entries[key]

        return (item, key)

    def remove(self, key):
        """
        """

        entry = self.entries.pop(key)
        entry[-2] = REMOVED

    def clean(self):
        """
        """

        self.heap = [entry for entry in self.heap if entry[-2] != REMOVED]

