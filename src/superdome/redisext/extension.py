import redis

from whodat.extension import Extension

class RedisExtension(Extension):
    """Extension that adds a Redis interface to request."""

    def __init__(self, connection_settings, attr_name):
        """Set the Redis interface."""
        self._attr_name = attr_name
        self._redis = redis.StrictRedis(connection_settings['host'], connection_settings['port'],
                                        password=connection_settings['password'])

    def process_request(self, request):
        """Add Redis interface to request."""
        setattr(request, self._attr_name, self._redis)
