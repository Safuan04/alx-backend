#!/usr/bin/python3
""" LFUCache  module
"""
import heapq
from base_caching import BaseCaching


class LFUCache(BaseCaching):
    def __init__(self):
        super().__init__()
        self.frequencies = {}  # Dictionary to store frequencies of elements
        self.counter = 0  # Counter for tiebreaking

    def update_frequencies(self, key):
        if key in self.frequencies:
            self.frequencies[key] += 1
        else:
            self.frequencies[key] = 1

    def put(self, key, item):
        if key is not None and item is not None:
            self.cache_data[key] = item
            self.update_frequencies(key)

        if len(self.cache_data) > self.MAX_ITEMS:
            removed_key = self.remove_least_frequent()
            print(f'DISCARD: {removed_key}')

    def get(self, key):
        if key is None or key not in self.cache_data:
            return None

        self.update_frequencies(key)
        return self.cache_data[key]

    def remove_least_frequent(self):
        min_key = min(self.frequencies, key=lambda k: (self.frequencies[k], self.counter))
        del self.cache_data[min_key]
        del self.frequencies[min_key]
        return min_key

    def __getitem__(self, key):
        # Overriding __getitem__ to increment the counter for tiebreaking
        self.counter += 1
        return super().__getitem__(key)
