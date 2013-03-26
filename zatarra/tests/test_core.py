#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests.test_core
   ~~~~~~~~~~~~~~~~~~~~~~~

"""


from zatarra.tests import BaseTestCase
from zatarra.core import QueueMaster
from zatarra.queue import Queue


class CoreQueueMasterDefaults(BaseTestCase):

    def test_initialization(self):
        """QueueMaster initialization defaults"""

        qm = QueueMaster()

        self.assertEqual({}, qm.queues)


class CoreQueueMasterAddTest(BaseTestCase):

    def test_add(self):
        """QueueMaster.add"""

        qm = QueueMaster()
        qm.add('moe')

        self.assertEqual(['moe'], qm.queues.keys())
        for q in qm.queues.values():
            self.assertIsInstance(q, Queue)

    def test_add_exists(self):
        """QueueMaster.add queue already exists"""

        qm = QueueMaster()
        qm.add('moe')

        with self.assertRaises(KeyError):
            qm.add('moe')

