#!/usr/bin/python
# -*- coding: utf-8 -*-

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

__author__ = 'flier'

setup(
    name = "tornado-rest-swagger",
    version = "0.8",
    packages = find_packages('src'),
    package_dir = {'':'src'},
    package_data = {
        'tornado_rest_swagger': ['assets/*/*'],
    },
    zip_safe = False,
    install_requires = [
        'tornado>=3.1',
        'epydoc>=0.3.1'
    ],
    author = "Flier Lu",
    author_email = "flier.lu@gmail.com",
    description = "Swagger Documentation Generator for the Tornado Web Framework",
    long_description = open('README').read(),
    license = "Apache",
    keywords = "tornado swagger api rest document",
    url = "http://github.com/flier/tornado_rest_swagger",
)