#!/usr/bin/python
# -*- coding: utf-8 -*-
import inspect

from enum import Enum, unique

from tornado.web import URLSpec

__author__ = 'flier'


@unique
class swagger_type(Enum):
    void = 0
    byte = 1
    boolean = 2
    int = 3
    long = 4
    float = 5
    double = 6
    string = 7
    date = 8
    complex = -1
    container = -2


class swagger_complex(object):
    def __init__(self):
        pass


class swagger_container(object):
    def __init__(self):
        pass


@unique
class swagger_param_type(Enum):
    path = 1
    query = 2
    body = 3
    header = 4
    form = 5


class swagger_param(object):
    def __init__(self, name, param_type=swagger_param_type.path, desc=None, data_type=None,
                 required=None, allowable_values=None, allow_multiple=False):
        self.name = name
        self.param_type = param_type
        self.desc = desc
        self.data_type = data_type
        self.required = required or param_type == swagger_param_type.path
        self.allowable_values = allowable_values
        self.allow_multiple = allow_multiple and param_type not in [swagger_param_type.path or swagger_param_type.body]


class rest_api(object):
    def __init__(self, name_or_func, response=None, summary=None, notes=None, errors=None, **kwds):
        if inspect.isfunction(name_or_func):
            self.__bind__(name_or_func)
            self.rest_api = self
            self.name = None
            self.summary = summary or name_or_func.__doc__
        else:
            self.func = None
            self.name = name_or_func
            self.summary = summary

        self.response = response

        self.notes = notes
        self.errors = errors
        self.kwds = kwds

    def __bind__(self, func):
        self.func = func

        self.__name__ = func.__name__
        self.func_args, self.func_varargs, self.func_keywords, self.func_defaults = inspect.getargspec(func)
        self.func_args = self.func_args[1:]

    def __call__(self, *args, **kwds):
        if self.func:
            return self.func(*args, **kwds)

        self.__bind__(args.pop(0))

        def __wrapper__(*args, **kwds):
            return self.func(*args, **kwds)

        __wrapper__.rest_api = self

        return __wrapper__

    @property
    def path(self):
        return self.url_spec._path % tuple(["{%s}" % arg for arg in self.func_args])


def find_rest_apis(host_handlers):
    for host, handlers in host_handlers:
        for spec in handlers:
            for (name, member) in inspect.getmembers(spec.handler_class):
                if inspect.ismethod(member) and hasattr(member, 'rest_api'):
                    member.rest_api.url_spec = spec

                    yield member.rest_api