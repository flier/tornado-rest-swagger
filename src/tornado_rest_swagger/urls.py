#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

import tornado.web

from views import SwaggerUIHandler, SwaggerResourcesHandler, SwaggerApiHandler

__author__ = 'flier'

ASSETS_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'assets')


def handle_urls(prefix):
    if prefix[-1] != '/':
        prefix += '/'

    return [
        tornado.web.URLSpec(prefix + r'$', SwaggerUIHandler, { 'assets_path': ASSETS_PATH }, name='swagger-api-doc'),
        tornado.web.URLSpec(prefix + r'api/$', SwaggerResourcesHandler, name='swagger-api-list'),
        (prefix + r'api/(?P<path>.*)/$', SwaggerApiHandler),

        (prefix + r'(.*\.(css|png|gif|js))', tornado.web.StaticFileHandler, { 'path': ASSETS_PATH }),
    ]