#!/usr/bin/env python3
'''Task 15's module.
'''
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


def print_top_ips(server_collection):
    """ Provides the most present IPs on Nginx logs stored in MongoDB. """
    print('IPs:')
    logs = server_collection.aggregate(
        [
            {
                '$group': {'_id': "$ip", 'totalRequests': {'$sum': 1}}
            },
            {
                '$sort': {'totalRequests': -1}
            },
            {
                '$limit': 10
            },
        ]
    )
    for log in logs:
        ip = log['_id']
        ip_counter = log['totalRequests']
        print('\t{}: {}'.format(ip, ip_counter))


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    print_nginx_stats(client.logs.nginx)
    print_top_ips(client.logs.nginx)
