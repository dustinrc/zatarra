#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.comms
   ~~~~~~~~~~~~~

"""


from gevent import monkey; monkey.patch_all()

from flask import Flask, jsonify, request
from gevent.pool import Pool
from gevent.pywsgi import WSGIServer

from zatarra.core import Zatarra


ADDRESS = ('', 2002)


comms = Flask(__name__)


def comms_server(address, backlog=1000, pool=None, log=None):
    """
    """

    kwargs = {
        'application': comms,
        'backlog': backlog,
        'spawn': pool or Pool(50000),
        'log': log,
    }

    return WSGIServer(address, **kwargs)


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


@comms.route('/queues/<name>/put')
def put(name):
    """
    """

    msg = {
        'data': None,
        'status': 'ok'
    }

    kwargs = dict(request.args.items())
    if 'priority' in kwargs:
        kwargs['priority'] = int(kwargs['priority'])
    del kwargs['item']

    z = Zatarra()
    msg['data'] = z.qm.put(name, request.args['item'], **kwargs)
    resp = jsonify(msg)

    return resp


@comms.route('/queues/<name>/get')
def get(name):
    """
    """

    msg = {
        'data': None,
        'status': 'ok'
    }

    z = Zatarra()
    msg['data'] = z.qm.get(name)
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

