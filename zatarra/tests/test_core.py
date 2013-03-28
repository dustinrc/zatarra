#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests.test_core
   ~~~~~~~~~~~~~~~~~~~~~~~

"""


from zatarra.tests import BaseTestCase
from zatarra.core import LOCAL_QUEUE, QueueMaster, Zatarra
from zatarra.queue import Queue


class CoreQueueMasterDefaultsTest(BaseTestCase):

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


class CoreQueueMasterDeleteTest(BaseTestCase):

    def test_delete(self):
        """QueueMaster.remove"""

        qm = QueueMaster()
        qm.add('moe')
        qm.delete('moe')

        self.assertEqual([], qm.queues.keys())

    def test_delete_non_existent(self):
        """QueueMaster.remove of non-existent queue"""

        qm = QueueMaster()

        with self.assertRaises(KeyError):
            qm.delete('moe')


class CoreQueueMasterPutTest(BaseTestCase):

    def test_put(self):
        """QueueMaster.put"""

        qm = QueueMaster()
        qm.add('moe')
        key = qm.put('moe', 1)

        self.assertEqual('00000000-0000-0000-0000-000000000001', key)
        self.assertEqual(1, len(qm.queues['moe']))

    def test_put_non_existent(self):
        """QueueMaster.put adds queue if non-existent"""

        qm = QueueMaster()
        key = qm.put('moe', 1)

        self.assertEqual('00000000-0000-0000-0000-000000000001', key)
        self.assertEqual(1, len(qm.queues['moe']))


class CoreQueueMasterGetTest(BaseTestCase):

    def test_get(self):
        """QueueMaster.get"""

        qm = QueueMaster()
        qm.put('moe', 1)

        expected_get = (1, '00000000-0000-0000-0000-000000000001')
        actual_get = qm.get('moe')

        self.assertEqual(expected_get, actual_get)

    def test_get_non_existent(self):
        """QueueMaster.get on non-existent queue"""

        qm = QueueMaster()

        with self.assertRaises(KeyError):
            qm.get('moe')


class CoreQueueMasterRemoveTest(BaseTestCase):

    def test_remove(self):
        """QueueMaster.remove"""

        qm = QueueMaster()
        key = qm.put('moe', 1)
        qm.put('larry', 1)
        qm.put('curly', 1)
        qm.remove(key)

        self.assertEqual(0, len(qm.queues['moe']))
        self.assertEqual(1, len(qm.queues['larry']))
        self.assertEqual(1, len(qm.queues['curly']))

    def test_remove_non_existent(self):
        """QueueMaster.remove of non-existent key"""

        qm = QueueMaster()

        with self.assertRaises(KeyError):
            qm.remove('')


class CoreZatarraDefaultsTest(BaseTestCase):

    def test_constants(self):
        """Zatarra constant defaults"""

        self.assertEqual('local', LOCAL_QUEUE)

    def test_initialization(self):
        """Zatarra initialization defaults"""

        z = Zatarra()

        self.assertEqual(['local'], z.qm.queues.keys())

    def test_initialization_singleton(self):
        """Zatarra is a singleton"""

        z1 = Zatarra()
        z2 = Zatarra()

        self.assertIs(z1, z2)

