#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests.test_comms
   ~~~~~~~~~~~~~~~~~~~~~~~~

"""


import requests

from zatarra.tests import BaseTestCase
from zatarra.comms import comms_server, ADDRESS
from zatarra.core import Zatarra


class CommsTestCase(BaseTestCase):

    def setUp(self):
        super(CommsTestCase, self).setUp()
        self.address = ('127.0.0.1', 2002)
        self.cs = comms_server(self.address)
        self.cs.start()

    def make_url(self, path):
        if path.startswith('/'):
            path = path[1:]

        return '/'.join(['http://{0}:{1}'.format(*self.address), path])

    def tearDown(self):
        self.cs.stop()
        z = Zatarra()
        z._drop()
        super(CommsTestCase, self).tearDown()


class CommsDefaultsTest(BaseTestCase):

    def test_constants(self):
        """Comms constant defaults"""

        self.assertEqual(('', 2002), ADDRESS)


class CommsQueueAddTest(CommsTestCase):

    def test_add(self):
        """Comms queue add"""

        url = self.make_url('/queues/moe/add')
        r = requests.get(url)

        expected = {
            'data': None,
            'status': 'ok'
        }
        actual = r.json()

        self.assertEqual(expected, actual)

    def test_add_existing(self):
        """Comms queue add, already exists"""

        url = self.make_url('/queues/moe/add')
        requests.get(url)
        r = requests.get(url)

        expected = {
            'data': None,
            'status': 'error'
        }
        actual = r.json()

        self.assertEqual(expected, actual)


class CommsQueueDeleteTest(CommsTestCase):

    def test_delete(self):
        """Comms queue delete"""

        add_url = self.make_url('/queues/moe/add')
        delete_url = self.make_url('/queues/moe/delete')
        requests.get(add_url)
        r = requests.get(delete_url)

        expected = {
            'data': None,
            'status': 'ok'
        }
        actual = r.json()

        self.assertEqual(expected, actual)

    def test_delete_non_existent(self):
        """Comms queue delete, non-existent"""

        url = self.make_url('/queues/moe/delete')
        r = requests.get(url)

        expected = {
            'data': None,
            'status': 'error'
        }
        actual = r.json()

        self.assertEqual(expected, actual)


class CommsQueuePutTest(CommsTestCase):

    def test_put(self):
        """Comms queue put"""

        url = self.make_url('/queues/moe/put?item=1')
        r = requests.get(url)

        expected = {
            'data': '00000000-0000-0000-0000-000000000001',
            'status': 'ok'
        }
        actual = r.json()

        self.assertEqual(expected, actual)

    def test_put_extra_args(self):
        """Comms queue put with priority and key"""

        url = self.make_url('/queues/moe/put?item=1')
        r = requests.get(url)
        key = r.json()['data']

        extras_url = self.make_url(
            '/queues/moe/put?item=2&priority=-1&key={}'.format(key)
        )
        extras_r = requests.get(extras_url)

        expected = {
            'data': '00000000-0000-0000-0000-000000000001',
            'status': 'ok'
        }
        actual = r.json()

        self.assertEqual(expected, actual)


class CommsQueueGetTest(CommsTestCase):

    def test_get(self):
        """Comms queue get"""

        url_put = self.make_url('/queues/moe/put?item=1')
        url_get = self.make_url('/queues/moe/get')
        requests.get(url_put)
        r = requests.get(url_get)

        expected = {
            'data': ['1', '00000000-0000-0000-0000-000000000001'],
            'status': 'ok'
        }
        actual = r.json()

        self.assertEqual(expected, actual)


class CommsHealthTest(CommsTestCase):

    def test_ping(self):
        """Comms basic 'ping'"""

        url = self.make_url('/health/ping')
        r = requests.get(url)

        expected = {
            'data': 'pong',
            'status': 'ok'
        }
        actual = r.json()

        self.assertEqual(expected, actual)
        self.assertEqual(200, r.status_code)

    def test_404(self):
        """Comms 404 on bad paths"""

        url = self.make_url('a/bad/path')
        r = requests.get(url)

        expected = {
            'data': 'not found: {}'.format(url),
            'status': 'error'
        }
        actual = r.json()

        self.assertEqual(expected, actual)
        self.assertEqual(404, r.status_code)

