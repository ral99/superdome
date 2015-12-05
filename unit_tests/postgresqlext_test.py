import unittest

from superdome.postgresqlext import PostgreSQLExtension
from whodat.handler import *
from whodat.http import *
from whodat.wsgi import *

### Settings ###

POSTGRESQL_CONNECTIONS = {
    'db': {
        'master': {
            'database': 'testing',
            'host': 'localhost',
            'port': 5432,
            'user': 'user',
            'password': 'user'
        },
        'slave': [
            {
                'database': 'testing',
                'host': 'localhost',
                'port': 5432,
                'user': 'user',
                'password': 'user'
            },
            {
                'database': 'testing',
                'host': 'localhost',
                'port': 5432,
                'user': 'user',
                'password': 'user'
            }
        ]
    }
}

### Handlers ###

@url('/')
class RootHandler:
    def get(self, request):
        db_conn = request.pgsql.get_slave_connection('db')
        with db_conn.open_cursor() as db_cursor:
            db_cursor.execute("SELECT DISTINCT name FROM names ORDER BY name")
            return ', '.join([row[0] for row in db_cursor.fetch_all()])

    def post(self, request):
        db_conn = request.pgsql.get_master_transactional_connection('db')
        with db_conn.open_cursor() as db_cursor:
            db_cursor.execute("INSERT INTO names (name) VALUES (%s)", ('Brees',))
            db_cursor.execute("INSERT INTO names (name) VALUES (%s)", ('Gleason',))
            db_cursor.execute("INSERT INTO names (name) VALUES (%s)", ('Graham',))
            db_conn.commit()
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
