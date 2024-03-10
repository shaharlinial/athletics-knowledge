class BaseController:

    def __init__(self, sql_connection):
        self.conn = sql_connection.connection
