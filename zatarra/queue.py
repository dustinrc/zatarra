#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.queue
   ~~~~~~~~~~~~~

"""


PRIORITY = 0
REMOVED = '<REMOVED>'


class Queue(object):
    """
    """

    def __init__(self):
        self.heap = []
        self.entries = {}

