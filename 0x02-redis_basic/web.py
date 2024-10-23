#!/usr/bin/env python3
""" This module defines a function name get_page. """

import redis
import requests
from functools import wraps
from typing import Callable


redis_storage = redis.Redis()


def cache(fn: Callable) -> Callable:
    """ Manages the caching for a request. """
    @wraps(fn)
    def caching(url: str) -> str:
        """ Caches the response content from a HTTP request. """
        redis_storage.incr(f"count:{url}")
        output = redis_storage.get(f"output:{url}")

        if output:
            return output.decode('utf-8')
        output = fn(url)
        redis_storage.set(f"count:{url}", 0)
        redis_storage.setex(f"output:{url}", 10, output)
        return output
    return caching


@cache
def get_page(url: str) -> str:
    """ Obtains the HTML content of an url. """
    return requests.get(url).text
