#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
   zatarra
   ~~~~~~~

   It means, "driftwood."
"""


from distutils.version import StrictVersion


__version__ = StrictVersion('0.1a0')


def version():
   """Provide the version as a string."""

   return str(__version__)

