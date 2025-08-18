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
   
    def join_many_to_many(self, association_table, related_col, related_id, main_col=None, association_main_col=None):

        main_col = main_col or "id"
        association_main_col = association_main_col or main_col

        if isinstance(related_id, int):
            self.filters.append(
                f"{main_col} IN (SELECT {association_main_col} FROM {association_table} WHERE {related_col} = ?)"
            )
            self.params.append(related_id)

        elif isinstance(related_id, (list, tuple, set)) and related_id:
            placeholders = ", ".join("?" for _ in related_id)
            self.filters.append(
                f"{main_col} IN (SELECT {association_main_col} FROM {association_table} WHERE {related_col} IN ({placeholders}))"
            )
            self.params.extend(related_id)

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
