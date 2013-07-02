#!/usr/bin/python
# -*- coding: utf-8 -*-
import urlparse

import tornado.web
import tornado.template

__author__ = 'flier'


class SwaggerUIHandler(tornado.web.RequestHandler):
    def initialize(self, assets_path):
        self.assets_path = assets_path

    def get_template_path(self):
        return self.assets_path

    def get(self):
        discovery_url = urlparse.urljoin(self.request.full_url(), self.reverse_url('swagger-api-list'))

        self.render('index.html', discovery_url=discovery_url)


class SwaggerResourcesHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class SwaggerApiHandler(tornado.web.RequestHandler):
    def get(self, path):
        pass
