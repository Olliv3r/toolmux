import sqlite3
from typing import List, Dict, Any

# Classe de abstração da tabela (Representa uma tabela)
class Table:
    def __init__(self, name: str, columns: List[str]):
        self.name = name
        self.columns = columns

    def __str__(self):
        return self.name


# Classe de abstração para construir uma consulta SQL
class Query:
    def __init__(self, table: Table):
        self.table = table
        self.select_columns = "*"
        self.filters = []
        self.order_by = ""
        self.limit = None

    def select(self, columns: List[str] = None):
        if columns:
            self.select_columns = ", ".join(columns)
        return self

    def where(self, **conditions: Dict[str, Any]):
        conditions_str = [f"{key} = ?" for key in conditions]
        self.filters.append(" AND ".join(conditions_str))
        self.filter_values = list(conditions.values())
        return self

    def order_by(self, columns: str, descendig: bool = False):
        self.order_by = f"ORDER BY {columns} {'DESC' if descendig else 'ASC'}"
        return self

    def limit(self, count: int):
        self.limit = f"LIMIT {count}"
        return self

    def build_query(self):
        query = f"SELECT {self.select_columns} FROM {self.table}"

        if self.filters:
            query += " where " + " AND ".join(self.filters)

        if self.order_by:
            query += " " + self.order_by

        if self.limit:
            query += " " + self.limit

        return query

    def execute(self, conn: sqlite3.Connection):
        query = self.build_query()
        print(f"Executing query: {query}")
        cursor = conn.cursor()
        cursor.execute(query, self.filter_values if hasattr(self, 'filter_values') else [])
        return cursor.fetchall()

def create_connection(db_name: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_name)
    return conn

def main():
    conn = create_connection('example.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS category (
        id INTEGER PRIMARY KEY,
        name TEXT
    )''')
    conn.execute("INSERT INTO category (name) VALUES ('Web Applications')")
    conn.execute("INSERT INTO category (name) VALUES ('Sniffing and Faking')")
    conn.execute("INSERT INTO category (name) VALUES ('Exploitation Tools')")
    conn.commit()

    category_table = Table("category", ["id", "name"])
    query = Query(category_table)

    result = query.select(["id", "name"]).where(name="Sniffing and Faking").order_by("id", descendig=True).limit(1).execute(conn)

    print("Results: ",result)
    conn.close()

if __name__ == "__main__":
    main()
