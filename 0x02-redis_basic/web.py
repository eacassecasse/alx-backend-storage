#!/usr/bin/env python3
""" This module defines a function name get_page. """

from typing import Callable
import redis
import requests
from functools import wraps


_redis = redis.Redis()


def cache(fn: Callable) -> Callable:
    """ Manages the caching for a request. """
    @wraps(fn)
    def caching(url) -> str:
        """ Caches the response content from a HTTP request. """
        _redis.incr("count:{}".format(url))
        output = _redis.get("response:{}".format(url))

        if output:
            return output.decode('utf-8')
        output = fn(url)
        _redis.set("count:{}".format(url), 0)
        _redis.setex("response:{}".format(url), 10, output)
        return output
    return caching


def get_page(url: str) -> str:
    """ Obtains the HTML content of an url. """
    return requests.get(url).text
