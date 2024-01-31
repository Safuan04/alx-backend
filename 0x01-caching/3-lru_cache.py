#!/usr/bin/env python3
""" LRUCache  module
"""
from base_caching import BaseCaching


class LRUCache(BaseCaching):
    """ LRUCache that inherits from BaseCaching
    -   and is a caching system
    """
    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.order = []

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

            if key in self.order:
                self.order.remove(key)
            self.order.append(key)

        if len(self.cache_data.items()) > self.MAX_ITEMS:
            removed_key = self.order.pop(0)
            self.cache_data.pop(removed_key)
            print(f'DISCARD: {removed_key}')

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        if key in self.order:
            self.order.remove(key)
        self.order.append(key)

        return self.cache_data.get(key)
