import sqlite3
from db import DB_PATH

class Connect:
    def __init__(self, db_name=DB_PATH):
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self._connect()

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.cursor = self.connection.cursor()

        except sqlite3.Error as error:
            print(f"Erro de conexão: {error}")

        except Exception as e:
            print(f"Erro inesperado na conexão: {e}")


    def commit(self):
        if self.connection:
            self.connection.commit()
            return True
            
        return False

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
            return True
        
        return False
