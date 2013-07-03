#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect

from functools import wraps

__author__ = 'flier'


class rest_api(object):
    def __init__(self, func_or_name, summary=None, notes=None, response=None, errors=None, **kwds):
        self.summary = summary
        self.notes = notes
        self.response = response
        self.errors = errors

        self.kwds = kwds

        if inspect.isfunction(func_or_name) or inspect.ismethod(func_or_name):
            self.__bind__(func_or_name)
            self.rest_api = self
            self.name = func_or_name.__name__
        elif isinstance(func_or_name, basestring):
            self.func = None
            self.name = func_or_name

    def __bind__(self, func):
        self.func = func

        self.__name__ = func.__name__
        self.func_args, self.func_varargs, self.func_keywords, self.func_defaults = inspect.getargspec(func)
        self.func_args = self.func_args

        if len(self.func_args) > 0 and self.func_args[0] == 'self':
            self.func_args = self.func_args[1:]

        if self.summary is None:
            self.summary = inspect.getcomments(self.func)

        if self.summary:
            self.summary = self.summary.strip()

        if self.notes is None:
            self.notes = inspect.getdoc(self.func)

        if self.notes:
            self.notes = self.notes.strip()

    def __call__(self, *args, **kwds):
        if self.func:
            return self.func(*args, **kwds)

        func = args[0]

        self.__bind__(func)

        @wraps(func)
        def __wrapper__(*args, **kwds):
            return self.func(*args, **kwds)

        __wrapper__.rest_api = self

        return __wrapper__

    @property
    def path(self):
        return self.url_spec._path % tuple(["{%s}" % arg for arg in self.func_args])


def discover_rest_apis(host_handlers):
    for host, handlers in host_handlers:
        for spec in handlers:
            for (name, member) in inspect.getmembers(spec.handler_class):
                if inspect.ismethod(member) and hasattr(member, 'rest_api'):
                    yield spec._path % tuple(['{%s}' % arg for arg in member.rest_api.func_args]), inspect.getdoc(spec.handler_class)

                    break


def find_rest_api(host_handlers, path):
    for host, handlers in host_handlers:
        for spec in handlers:
            for (name, member) in inspect.getmembers(spec.handler_class):
                if inspect.ismethod(member) and hasattr(member, 'rest_api'):
                    spec_path = spec._path % tuple(['{%s}' % arg for arg in member.rest_api.func_args])

                    if path == spec_path[1:]:
                        operations = [member.rest_api for (name, member) in inspect.getmembers(spec.handler_class) if hasattr(member, 'rest_api')]

                        return spec, operations

                    continue
