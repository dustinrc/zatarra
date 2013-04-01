#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.comms
   ~~~~~~~~~~~~~

"""


from gevent import monkey; monkey.patch_all()

from flask import Flask, jsonify, request
from gevent.pywsgi import WSGIServer

from zatarra.core import Zatarra


ADDRESS = ('', 2002)


comms = Flask(__name__)


def comms_server(address):
    """
    """

    return WSGIServer(address, application=comms, log=None)


@comms.route('/queues/<name>/add')
def add(name):
    """
    """

    msg = {
        'data': None,
        'status': 'ok'
    }

    z = Zatarra()

    try:
        z.qm.add(name)
    except KeyError:
        msg['status'] = 'error'

    resp = jsonify(msg)

    return resp


@comms.route('/queues/<name>/delete')
def delete(name):
    """
    """

    msg = {
        'data': None,
        'status': 'ok'
    }

    z = Zatarra()

    try:
        z.qm.delete(name)
    except KeyError:
        msg['status'] = 'error'

    resp = jsonify(msg)

    return resp


@comms.route('/health/ping')
def ping():
    """
    """

    msg = {
        'data': 'pong',
        'status': 'ok'
    }

    resp = jsonify(msg)

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

