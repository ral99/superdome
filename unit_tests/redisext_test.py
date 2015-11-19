import unittest

from superdome.redisext import RedisExtension
from whodat.handler import *
from whodat.http import *
from whodat.wsgi import *

### Settings ###

REDIS_CONNECTION = {
    'host': 'localhost',
    'port': 6379,
    'password': None
}

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        return request.redis.get("chant").decode('utf-8')

    def post(self, request):
        request.redis.set("chant", "Who dat? Who dat? Who dat say dey gonna beat dem Saints?")
        return ''

### Tests ###

class PostgreSQLExtensionTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(False, extensions=[RedisExtension(REDIS_CONNECTION, 'redis')])
        self.app.add_handler(RootHandler)

    def test_connection(self):
        request = HTTPRequest.post(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')

        request = HTTPRequest.get(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.text, "Who dat? Who dat? Who dat say dey gonna beat dem Saints?")

if __name__ == '__main__':
    unittest.main()
