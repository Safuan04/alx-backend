#!/usr/bin/env python3
""" FIFOCache  module
"""
from base_caching import BaseCaching


class FIFOCache(BaseCaching):
    """ FIFOCache that inherits from BaseCaching
    -   and is a caching system
    """
    def put(self, key, item):
        """ Add an item in the cache
        """
        if key is not None and item is not None:
            self.cache_data[key] = item

        first_key = next(iter(self.cache_data))

        if len(self.cache_data.items()) > self.MAX_ITEMS:
            self.cache_data.pop(first_key)
            print(f'DISCARD: {first_key}')

    def get(self, key):
        """ Get an item by key
        """
        if key is None or key not in self.cache_data:
            return None

        return self.cache_data.get(key)
