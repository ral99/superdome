import unittest

from superdome.sqliteext import SQLiteExtension
from whodat.handler import *
from whodat.http import *
from whodat.wsgi import *

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        sqlite_cursor = request.sqlite_conn.cursor()
        sqlite_cursor.execute("CREATE TABLE t(id INT PRIMARY KEY NOT NULL);")
        sqlite_cursor.execute("INSERT INTO t(id) VALUES(42);")
        request.sqlite_conn.commit()
        return ''

    def post(self, request):
        sqlite_cursor = request.sqlite_conn.cursor()
        sqlite_cursor.execute("SELECT * FROM t;")
        return str(sqlite_cursor.fetchone()['id'])

### Tests ###

class SQLiteExtensionTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(False, extensions=[SQLiteExtension(':memory:', 'sqlite_conn')])
        self.app.add_handler(RootHandler)

    def test_connection(self):
        request = HTTPRequest.get(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')

        request = HTTPRequest.post(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.text, "42")

if __name__ == '__main__':
    unittest.main()
