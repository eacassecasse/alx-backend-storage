#!/usr/bin/env python3
""" This module defines a function print_nginx_stats. """
from pymongo import MongoClient


def print_nginx_stats(collection):
    """ Provides some stats about Nginx logs stored in MongoDB. """
    print('{} logs'.format(collection.count_documents({})))
    print('Methods:')
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(collection.find({'method': method})))
        print('\tmethod {}: {}'.format(method, req_count))
    status_counter = len(list(
        collection.find({'method': 'GET', 'path': '/status'})
    ))
    print('{} status check'.format(status_counter))


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_stats(client.logs.nginx)
