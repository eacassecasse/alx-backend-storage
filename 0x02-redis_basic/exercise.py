#!/usr/bin/env python3
""" This module defines a class named Cache. """

from functools import wraps
from typing import Callable, Union
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """ Keeps track of the amount of times a function was called. """
    @wraps(method)
    def increment(self, *args, **kwargs):
        """ Increments the number of calls on each call. """
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, *kwargs)
    return increment


def call_history(method: Callable) -> Callable:
    """ Keeps track of the call history for a particular function. """
    @wraps(method)
    def push_history(self, *args, **kwargs):
        """ Stores the history of inputs and outputs of a function call. """
        input_key = "{}:inputs".format(method.__qualname__)
        output_key = "{}:outputs".format(method.__qualname__)
        output = method(self, *args, *kwargs)

        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(input_key, str(args))
            self._redis.rpush(output_key, output)
        return output
    return push_history


def replay(method: Callable) -> None:
    """ Displays the history of calls of a particular function. """
    if method is None or not hasattr(method, '__self__'):
        return
    _redis = getattr(method.__self__, '_redis', None)
    if not isinstance(_redis, redis.Redis):
        return
    method_name = method.__qualname__
    input_key = '{}:inputs'.format(method_name)
    output_key = '{}:outputs'.format(method_name)
    calls_counter = 0
    if _redis.exists(method_name) != 0:
        calls_counter = int(_redis.get(method_name))
    print('{} was called {} times:'.format(method_name, calls_counter))
    inputs = _redis.lrange(input_key, 0, -1)
    outputs = _redis.lrange(output_key, 0, -1)
    for input, output in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            method_name,
            input.decode("utf-8"),
            output,
        ))


class Cache:
    """ The Cache Model """
    def __init__(self):
        """ Initializes a new cache instance. """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Stores a data under a random UUID key on Redis. """
        key = str(uuid.uuid4())
        # if isinstance(data, (int, float)):
        #     data = str(data)
        self._redis.set(key, data)
        return key

    def get(
            self,
            key: str,
            fn: Callable = None
            ) -> Union[str, bytes, int, float]:
        """ Retrieves a byte value Redis Storage and converts to
        a format specified by fn.
        """
        data = self._redis.get(key)
        if fn is not None:
            data = fn(data)
        return data

    def get_str(self, key: str) -> str:
        """ Retrieves a string from Redis Storage. """
        return self.get(key, lambda value: value.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """ Retrieves an integer from Redis Storage. """
        return self.get(key, lambda value: int(value))
