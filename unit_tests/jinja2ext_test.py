import unittest

from superdome.jinja2ext import Jinja2Extension
from whodat.handler import *
from whodat.http import *
from whodat.wsgi import *

### Settings ###

TEMPLATE_DIR = 'unit_tests/templates'

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        return request.jinja2.render('index.html', {'method': 'get'})

    def post(self, request):
        return request.jinja2.render('index.html', {'method': 'post'})

### Tests ###

class Jinja2ExtensionTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(False, extensions=[Jinja2Extension(TEMPLATE_DIR, 'jinja2')])
        self.app.add_handler(RootHandler)

    def test_render(self):
        request = HTTPRequest.get(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.text, 'Method is get')

        request = HTTPRequest.post(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.text, 'Method is post')

if __name__ == '__main__':
    unittest.main()
