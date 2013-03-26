#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.comms
   ~~~~~~~~~~~~~

"""


from gevent import monkey; monkey.patch_all()

from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer


ADDRESS = ('', 2002)


comms = Flask(__name__)


def comms_server(address):
    """
    """

    return WSGIServer(address, comms)


@comms.route('/health/ping')
def ping():
    """
    """

    msg = {
        'data': 'pong',
        'status': 'ok'
    }

    resp = jsonify(msg)
    resp.status_code = 200

    return resp


@comms.errorhandler(404)
def not_found(error=None):
    """
    """

    msg = {
        'data': 'not found: {}'.format(request.url),
        'status': 'error'
    }

    resp = jsonify(msg)
    resp.status_code = 404

    return resp

