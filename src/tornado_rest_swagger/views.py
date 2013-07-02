#!/usr/bin/python
# -*- coding: utf-8 -*-
import tornado.web

__author__ = 'flier'


class SwaggerUIHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class SwaggerResourcesHandler(tornado.web.RequestHandler):
    def get(self):
        pass


class SwaggerApiHandler(tornado.web.RequestHandler):
    def get(self, path):
        pass
