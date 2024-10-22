#!/usr/bin/env python3
""" This module defines a function `schools_by_topic`. """


def schools_by_topic(mongo_collection, topic):
    """ Returns the list of school having a specific topic. """
    filtr = {
        'topics': {
            '$elemMatch': {
                '$eq': topic,
            },
        },
    }
    return [d for d in mongo_collection.find(filtr)]
