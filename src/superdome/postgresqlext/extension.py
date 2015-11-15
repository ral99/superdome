from pgwizard import PostgreSQLConnection, PostgreSQLConnectionPool
from whodat.extension import Extension

class PostgreSQLExtension(Extension):
    """Extension that adds a pool of PostgreSQL databases connections to request."""

    def __init__(self, connections_settings, attr_name):
        """Set the pool of connections."""
        self._attr_name = attr_name
        self._pool = PostgreSQLConnectionPool()
        for name, connections in connections_settings.items():
            for connection in connections:
                self._pool.add_connection(
                        name,
                        PostgreSQLConnection(connection['database'], connection['host'], connection['port'],
                                             connection['user'], connection['password'], connection['accept_writes'],
                                             connection['accept_reads'], connection['autocommit'],
                                             connection['max_connection_age_in_seconds'])
                )

    def process_request(self, request):
        """Refresh connections, open cursors and set a connection pool attribute in request."""
        self._pool.refresh_connections()
        self._pool.open_cursors()
        setattr(request, self._attr_name, self._pool)

    def process_response(self, request, response):
        """Close cursors."""
        self._pool.close_cursors()
