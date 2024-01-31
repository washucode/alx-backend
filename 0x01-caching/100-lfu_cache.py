#!/usr/bin/env python3
""" LFUCache module
"""

from base_caching import BaseCaching


class LFUCache(BaseCaching):
    """
    LFUCache defines:
      - Caching system inherit from BaseCaching
    """

    def __init__(self):
        """ Initiliaze
        """
        super().__init__()
        self.cache_data = {}
        self.lfu = {}

    def put(self, key, item):
        """ Add an item in the cache
        """
        if key and item:
            # if key exists, update the value
            if key in self.cache_data:
                self.cache_data[key] = item
                self.lfu[key] += 1
            else:
                if len(self.cache_data) >= BaseCaching.MAX_ITEMS:
                    # get the least frequently used item
                    discard = min(self.lfu, key=self.lfu.get)
                    del self.cache_data[discard]
                    del self.lfu[discard]
                    print("DISCARD: {}".format(discard))
                self.cache_data[key] = item
                self.lfu[key] = 0

    def get(self, key):
        """ Get an item by key
        """
        if key in self.cache_data:
            self.lfu[key] += 1
            return self.cache_data[key]
        return None
