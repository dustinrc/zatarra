#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.core
   ~~~~~~~~~~~~

"""


from zatarra.util import  Singleton
from zatarra.queue import PRIORITY, Queue


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

    def delete(self, name):
        """
        """

        try:
            del self.queues[name]
        except KeyError:
            raise KeyError('queue {} does not exist'.format(name))

    def put(self, name, item, priority=PRIORITY, key=None):
        """
        """

        if name not in self.queues:
            self.add(name)

        key = self.queues[name].put(item, priority=priority, key=key)

        return key

    def get(self, name):
        """
        """

        if name not in self.queues:
            raise KeyError('queue {} does not exist'.format(name))

        return self.queues[name].get()

    def remove(self, key):
        """
        """

        for name in self.queues:
            try:
                self.queues[name].remove(key)
                return
            except KeyError:
                continue

        raise KeyError('no queue contains key: {}'.format(key))

    def clean(self):
        """
        """

        for name in self.queues:
            self.queues[name].clean()


class Zatarra(object):
    """
    """

    __metaclass__ = Singleton

    def __init__(self):
        self.qm = QueueMaster()
        self.qm.add(LOCAL_QUEUE)

    @classmethod
    def _drop(cls):
        """
        Drop the instance (for testing purposes).
        """
        del cls._instance

