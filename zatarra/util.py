#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra.util
   ~~~~~~~~~~~~

"""


class Singleton(type):

    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance

