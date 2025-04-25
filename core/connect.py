import sqlite3
from db import DB_PATH

class Connect:
  def __init__(self, db_name=DB_PATH):
    try:
      self.connect = sqlite3.connect(db_name)
      self.cursor = self.connect.cursor()
      
    except sqlite3.Error as error:
      return error
      
    except:
      return False

  def commit(self):
    if self.connect:
      self.connect.commit()
      return True
      
    else:
      return False

  def close(self):
    if self.connect:
      self.connect.close()
      return True
      
    else:
      return False

