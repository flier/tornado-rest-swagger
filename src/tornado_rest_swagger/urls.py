#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

import tornado.web

from views import SwaggerUIHandler, SwaggerResourcesHandler, SwaggerApiHandler

__author__ = 'flier'

ASSETS_PATH = os.path.join(os.path.normpath(__file__), 'assets')


def handle_urls(prefix=''):
    return [
        (prefix + r'$', SwaggerUIHandler),
        (prefix + r'/api-docs/$', SwaggerResourcesHandler),
        (prefix + r'/api-docs/(?P<path>.*)/$', SwaggerApiHandler),

        (prefix + r'/assets/(.*)', tornado.web.StaticFileHandler, { 'path': ASSETS_PATH }),
    ]