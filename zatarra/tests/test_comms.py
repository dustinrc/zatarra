#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.tests.test_comms
   ~~~~~~~~~~~~~~~~~~~~~~~~

"""


import requests

from zatarra.tests import BaseTestCase
from zatarra.comms import comms_server, ADDRESS


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
        super(CommsTestCase, self).tearDown()


class CommsDefaultsTest(BaseTestCase):

    def test_constants(self):
        """Comms constant defaults"""

        self.assertEqual(('', 2002), ADDRESS)


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

