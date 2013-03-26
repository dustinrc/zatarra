#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.core
   ~~~~~~~~~~~~

"""


from zatarra.queue import Queue


class QueueMaster(object):
    """
    """

    def __init__(self):
        self.queues = {}

    def add(self, name):
        """
        """

        if name not in self.queues:
            self.queues[name] = Queue()
        else:
            raise KeyError('queue {} already exists'.format(name))

