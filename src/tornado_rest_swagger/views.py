#!/usr/bin/python
# -*- coding: utf-8 -*-
import urlparse
import json

import tornado.web
import tornado.template

from tornado_rest_swagger.settings import SWAGGER_VERSION, URL_SWAGGER_API_LIST
from tornado_rest_swagger.declare import find_rest_apis

__author__ = 'flier'


def json_dumps(obj, pretty=False):
    return json.dumps(obj, sort_keys=True, indent=4, separators=(',', ': ')) if pretty else json.dumps(obj)


class SwaggerUIHandler(tornado.web.RequestHandler):
    def initialize(self, assets_path, **kwds):
        self.assets_path = assets_path

    def get_template_path(self):
        return self.assets_path

    def get(self):
        discovery_url = urlparse.urljoin(self.request.full_url(), self.reverse_url(URL_SWAGGER_API_LIST))

        self.render('index.html', discovery_url=discovery_url)


class SwaggerResourcesHandler(tornado.web.RequestHandler):
    """
    Swagger Resource Listing

    https://github.com/wordnik/swagger-core/wiki/Resource-Listing
    """

    def initialize(self, api_version, exclude_namespaces, **kwds):
        self.api_version = api_version
        self.exclude_namespaces = exclude_namespaces

    def get(self):
        self.set_header('content-type', 'application/json')

        resources = {
            'apiVersion': self.api_version,
            'swaggerVersion': SWAGGER_VERSION,
            'basePath': self.request.full_url(),
            'apis': [{'path': api.path, 'description': api.summary} for api in find_rest_apis(self.application.handlers)]
        }

        self.finish(json_dumps(resources, self.get_arguments('pretty')))


class SwaggerApiHandler(tornado.web.RequestHandler):
    """
    Swagger API Declaration

    https://github.com/wordnik/swagger-core/wiki/API-Declaration
    """

    def get(self, path):
        self.set_header('content-type', 'application/json')

        api_spec = {

        }

        self.finish(json_dumps(api_spec, self.get_arguments('pretty')))