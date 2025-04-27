# Classe abstrata para construir consultas SQL
class QueryBuilder:
    def __init__(self, table_name, connection=None):
        self.table_name = table_name
        self.connection = connection
        self.filters = []
        self.params = []
        self.order = None
        self.limit_value = None
        self._count = None
        self.columns = "*"

    def select_columns(self, *columns):
        self.columns = ", ".join(columns)
        return self

    def filter_by(self, **kwargs):
        for key, value in kwargs.items():
            self.filters.append(f"{key} = ?")
            self.params.append(value)
        return self
        
    def where(self, condition):
        self.filters.append(condition)
        return self

    def order_by(self, column_name):
        self.order = column_name
        return self

    def limit(self, number):
        self.limit_value = number
        return self

    def count(self):
        self._count = True
        return self

    def build_query(self):
        if self._count:
            query = f"SELECT COUNT(*) FROM {self.table_name}"
        else:
            query = f"SELECT {self.columns} FROM {self.table_name}"

        if self.filters:
            query += " WHERE " + " AND ".join(self.filters)
            
        if not self._count:
            if self.order:
                query += f" ORDER BY {self.order}"

            if self.limit_value:
                query += f" LIMIT {self.limit_value}"

        return query

    def execute(self, params=None):
        query = self.build_query()
        self.connection.cursor.execute(query, self.params)

        if self._count:
            return self.connection.cursor.fetchone()[0]

        if self.columns != "*":
            result = self.connection.cursor.fetchone()

            if result:
                return result[0]
            return None
            
        else:
            return self.connection.cursor.fetchall()
