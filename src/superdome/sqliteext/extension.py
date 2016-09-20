import sqlite3

from whodat.extension import Extension

class SQLiteExtension(Extension):
    """Extension that adds a SQLite connection to request."""

    def __init__(self, database, attr_name):
        """Set up the connection with database."""
        self._attr_name = attr_name
        self._connection = sqlite3.connect(database)

    def process_request(self, request):
        """Set the connection attribute in request."""
        setattr(request, self._attr_name, self._connection)
