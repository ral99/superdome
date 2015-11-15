import unittest

from superdome.postgresqlext import PostgreSQLExtension
from whodat.handler import *
from whodat.http import *
from whodat.wsgi import *

### Settings ###

POSTGRESQL_CONNECTIONS = {
    'db': [
        {
            'database': 'testing',
            'host': 'localhost',
            'port': 5432,
            'user': 'user',
            'password': 'user',
            'accept_writes': True,
            'accept_reads': True,
            'autocommit': False,
            'max_connection_age_in_seconds': None
        },
    ]
}

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        conn = request.pgsql.get_connection_for_reading_from('db')
        conn.execute("SELECT DISTINCT name FROM names ORDER BY name")
        return ', '.join([row[0] for row in conn.fetch_all()])

    def post(self, request):
        conn = request.pgsql.get_connection_for_writing_to('db')
        conn.execute("INSERT INTO names (name) VALUES (%s)", ('Brees',))
        conn.execute("INSERT INTO names (name) VALUES (%s)", ('Gleason',))
        conn.execute("INSERT INTO names (name) VALUES (%s)", ('Graham',))
        conn.commit()
        return ''

### Tests ###

class PostgreSQLExtensionTest(unittest.TestCase):
    def setUp(self):
        self.app = WSGIApplication(False, extensions=[PostgreSQLExtension(POSTGRESQL_CONNECTIONS, 'pgsql')])
        self.app.add_handler(RootHandler)

    def test_connection(self):
        request = HTTPRequest.post(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')

        request = HTTPRequest.get(path_info='/')
        response = self.app.handle_request(request)
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.text, 'Brees, Gleason, Graham')

if __name__ == '__main__':
    unittest.main()
