#!/usr/bin/python
# -*- coding: utf-8 -*-
import urlparse
import json

import tornado.web
import tornado.template

from tornado_rest_swagger.settings import SWAGGER_VERSION, URL_SWAGGER_API_LIST
from tornado_rest_swagger.declare import discover_rest_apis, find_rest_api

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

        apis = [{
            'path': path,
            'description': desc
        } for path, desc in discover_rest_apis(self.application.handlers)]

        u = urlparse.urlparse(self.request.full_url())

        resources = {
            'apiVersion': self.api_version,
            'swaggerVersion': SWAGGER_VERSION,
            'basePath': '%s://%s%s' % (u.scheme, u.netloc, u.path),
            'apis': apis
        }

        self.finish(json_dumps(resources, self.get_arguments('pretty')))


class SwaggerApiHandler(tornado.web.RequestHandler):
    """
    Swagger API Declaration

    https://github.com/wordnik/swagger-core/wiki/API-Declaration
    """

    def initialize(self, api_version, **kwds):
        self.api_version = api_version

    def get(self, path):
        spec, apis = find_rest_api(self.application.handlers, path)

        u = urlparse.urlparse(self.request.full_url())

        spec = {
            'apiVersion': self.api_version,
            'swaggerVersion': SWAGGER_VERSION,
            'basePath': '%s/%s%s' % (u.scheme, u.netloc, u.path),
            'apis': [{
                'path': '/' + path,
                'description': spec.handler_class.__doc__,
                'operations': [{
                    'httpMethod': api.func.__name__.upper(),
                    'nickname': api.name,
                    'parameters': [],
                    'summary': api.summary,
                    'notes': api.notes,
                    'responseClass': api.response,
                    'errorResponses': api.errors,
                } for api in apis]
            }]
        }

        self.set_header('content-type', 'application/json')

        self.finish(json_dumps(spec, self.get_arguments('pretty')))
