import sqlite3
from core.connect import Connect
from db import DB_PATH

class Tool:
  def __init__(self, tb_name = "tool"):
    self.tb_name = tb_name
    self.db = Connect()
      
  def sq(self, sql, params=None):
    try:
        result = self.db.cursor.execute(sql, params)
        return result
      
    except sqlite3.Error as error:
        print(f"Erro na query: {error}")
        return False

  def get_total_tools(self):
        return self.sq(f'select count(*) from {self.tb_name}', ())
