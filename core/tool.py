from core.connect import Connect
from core.query_builder import QueryBuilder

class Tool:
    def __init__(self, tb_name="tool", connect=None):
        self.tb_name = tb_name
        self.db = connect or Connect()

    def select(self):
        return QueryBuilder(self.tb_name, connection=self.db)
