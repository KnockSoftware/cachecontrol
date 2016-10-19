class DjangoCache(object):
    """Allows use of a Django cache for CacheControl request caching

    Example:

    ```
    import requests
    from cachecontrol import CacheControl
    from cachecontrol.caches import DjangoCache

    session = CacheControl(requests.Session(), cache=DjangoCache('mycachename'))
    response = session.get('https://www.google.com')
    ```
    """
    def __init__(self, cache_name=None, cache=None, default_timeout=60*60*24*30):
        """Initialize with a named cache or a Django-compatible cache object

        The default timeout should be non-None so that, e.g., the redis LRU algorithm
        can eject stale cache entries
        """
        self.cache = cache
        self.default_timeout = default_timeout
        if self.cache is None:
            from django.core.cache import caches
            self.cache = caches[cache_name]

    def get(self, key):
        return self.cache.get(key)

    def set(self, key, value):
        self.cache.set(key, value, self.default_timeout)

    def delete(self, key):
        self.cache.delete(key)
