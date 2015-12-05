from pgwizard import PGWizardConnectionPool
from whodat.extension import Extension

class PostgreSQLExtension(Extension):
    """Extension that adds a pool of PostgreSQL databases connections to request."""

    def __init__(self, connections_settings, attr_name):
        """Set the pool of connections."""
        self._attr_name = attr_name
        self._pool = PGWizardConnectionPool()
        for name, connection in connections_settings.items():
            if 'master' in connection:
                master = connection['master']
                self._pool.set_master_database_server(name, master['database'], master['host'], master['port'],
                                                      master['user'], master['password'])
            for slave in connection.get('slave', []):
                self._pool.add_slave_database_server(name, slave['database'], slave['host'], slave['port'],
                                                     slave['user'], slave['password'])

    def process_request(self, request):
        """Set the pool of PostgreSQL databases connections attribute in request."""
        setattr(request, self._attr_name, self._pool)
