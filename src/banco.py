import sqlite3

class Connect:
  def __init__(self, db_name):
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


class Tool:
  tb_name = "tools"

  def __init__(self):
    self.tb_name = Tool.tb_name
    self.db = Connect('app.db')
      
  def instrunction(self, sql=f'select * from {tb_name} order by name'):
    try:
      result = self.db.cursor.execute(sql)
      return result
    except sqlite3.Error as error:
      return False

  def get_total_tool(self):
    return self.instrunction(f'select count(*) from {self.tb_name}')
