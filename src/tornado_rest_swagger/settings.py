#!/usr/bin/python
# -*- coding: utf-8 -*-
import os.path

__author__ = 'flier'

SWAGGER_VERSION = '1.1.15'

URL_SWAGGER_API_DOCS = 'swagger-api-docs'
URL_SWAGGER_API_LIST = 'swagger-api-list'
URL_SWAGGER_API_SPEC = 'swagger-api-spec'

ASSETS_PATH = os.path.join(os.path.dirname(os.path.normpath(__file__)), 'assets')

default_settings = {
    'assets_path': ASSETS_PATH,

    'api_version': '',
    'api_key': '',
    'enabled_methods': ['get', 'post', 'put', 'patch', 'delete'],
    'exclude_namespaces': [],
}