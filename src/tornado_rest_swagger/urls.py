#!/usr/bin/python
# -*- coding: utf-8 -*-
from tornado.web import URLSpec, StaticFileHandler

from tornado_rest_swagger.settings import default_settings, \
    URL_SWAGGER_API_DOCS, URL_SWAGGER_API_LIST, URL_SWAGGER_API_SPEC, ASSETS_PATH
from tornado_rest_swagger.views import SwaggerUIHandler, SwaggerResourcesHandler, SwaggerApiHandler

__author__ = 'flier'


def handle_urls(prefix, **opts):
    if prefix[-1] != '/':
        prefix += '/'

    default_settings.update(opts)

    return [
        URLSpec(prefix + r'$',                  SwaggerUIHandler,        default_settings, name=URL_SWAGGER_API_DOCS),
        URLSpec(prefix + r'api/$',              SwaggerResourcesHandler, default_settings, name=URL_SWAGGER_API_LIST),
        URLSpec(prefix + r'api/(?P<path>.*)/$', SwaggerApiHandler,       default_settings, name=URL_SWAGGER_API_SPEC),

        (prefix + r'(.*\.(css|png|gif|js))',    StaticFileHandler,       { 'path': ASSETS_PATH }),
    ]