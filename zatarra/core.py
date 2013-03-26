#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.core
   ~~~~~~~~~~~~

"""


from zatarra.util import  Singleton
from zatarra.queue import Queue


LOCAL_QUEUE = 'local'


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


class Zatarra(object):
    """
    """

    __metaclass__ = Singleton

    def __init__(self):
        self.qm = QueueMaster()
        self.qm.add(LOCAL_QUEUE)

