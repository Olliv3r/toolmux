import sqlite3
import io

class Connect:
    def __init__(self, db_name):
        try:
            self.db_name = db_name
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
            self.cursor.execute("SELECT SQLITE_VERSION()")
            self.data = self.cursor.fetchone()

        except sqlite3.Error:
            return False

    def commit_db(self):
        if self.conn:
            self.conn.commit()
            return True
        else:
            return False

    def close_db(self):
        if self.conn:
            self.conn.close()
            return True
        else:
            return False

    
class Tools:

    tb_name = "Tools"

    def __init__(self):
        self.db = Connect('banco.db')
        self.tb_name
        self.create_table()

    def close_connect(self):
        self.db.close_db()

        
    ### Cria tabela a partir do schema salvo
    
    def create_schema(self, schema_name='tools.sql'):
        try:
            with open(schema_name, 'rt') as f:
                schema = f.read()
                self.db.cursor.executescript(schema)

        except sqlite3.Error:
            return False

        
    ### Cria estrutura da tabela

    def create_table(self):
        sql = f"""CREATE TABLE IF NOT EXISTS {self.tb_name} (
        id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
        name TEXT NOT NULL,
        alias TEXT NOT NULL,
        link TEXT NULL,
        category TEXT NOT NULL,
        dependencies TEXT NULL,
        name_installer TEXT NULL,
        type_install TEXT NOT NULL
        );
        """
        self.db.cursor.execute(sql)

        
    ### Cadastra uma ferramenta
    
    def register_tool(self, data):

        try:
            self.db.cursor.execute(f"""
            INSERT INTO {self.tb_name} (
            name,
            alias,
            link,
            category,
            dependencies,
            name_installer,
            type_install) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
            self.db.conn.commit()
            return True

        except sqlite3.OperationalError as err:
            return err

        except sqlite3.IntegrityError as err:
            return err
    
    ### Seleciona todas as ferramentas ordernadas pelo id
    
    def select(self):
        try:
            sql = f"""
            SELECT * FROM {self.tb_name} ORDER BY id
            """
            result = self.db.cursor.execute(sql)
            return result.fetchall()
        
        except sqlite3.OperationalError as err:
            return err
    
    ### Localiza uma ferramenta
    
    def find_tool(self, ID):
        sql = f"""
        SELECT * FROM {self.tb_name} WHERE id = ?
        """
        result = self.db.cursor.execute(sql, (ID,))
        return result.fetchall()

    
    ### Visualiza uma ferramenta
    
    def view_tool(self, ID):
        if self.find_tool(ID) == None:
            return False
        else:
            return self.find_tool(ID)

        
    ### Visualiza todas as ferramentas
    
    def view_tools(self):
        
        if self.select() == None:
            return False
        else:
            return self.select()

        
    ### Visualizar total de ferramentas
    
    def view_total_tools(self):
        sql = f"""
        SELECT COUNT(*) FROM {self.tb_name}
        """
        result = self.db.cursor.execute(sql)
        return result.fetchone()[0]
    
    ### Select personalizado

    def custom_selection(self, sql=f"SELECT * FROM {tb_name} ORDER BY name"):
        try:
            result = self.db.cursor.execute(sql)
            self.db.conn.commit()
            return result.fetchall()

        except sqlite3.OperationalError as err:
            return err

    
    #### Atualiza dados de uma ferramenta
    
    def update_tool(self, data, ID):
        try:
            sql = f"""
            UPDATE {self.tb_name} SET name = ?, alias = ?, link = ?, category = ?, dependencies = ?, name_installer = ?, type_install = ? WHERE id = ?;
            """
            self.db.cursor.execute(sql, (data[0], data[1], data[2], data[3], data[4], data[5], data[6] ,ID))
            self.db.commit_db()
            return True
            
        except sqlite3.OperationalError as err:
            return err
        

    ### Renomeia uma coluna
    
    def rename_column(self, column_old, column_new):
        try:
            sql = f"""
            ALTER TABLE {self.tb_name} RENAME COLUMN {column_old} TO {column_new};
            """
            self.db.cursor.execute(sql)
            self.db.commit_db()
            return True

        except sqlite3.OperationalError as err:
            return err


    ### Apaga uma ferramenta
    
    def delete_tool(self, ID):
        try:
            c = self.find_tool(ID)

            if c:
                sql = f"""
                DELETE FROM {self.tb_name} WHERE id = ?
                """
                self.db.cursor.execute(sql, (ID,))
                self.db.commit_db()
                return True

            else:
                return False

        except sqlite3.OperationalError as err:
            return err

        
    ### Adicionar uma coluna
    
    def add_column(self, column):
        try:
            sql = f"""
            ALTER TABLE {self.tb_name} ADD COLUMN {column}
            """
            self.db.cursor.execute(sql)
            self.db.commit_db()
            return True
        
        except sqlite3.OperationalError as err:
            return err


    ### Apaga uma coluna
    
    def delete_column(self, column):
        try:
            sql = f"""
            ALTER TABLE {self.tb_name} DROP COLUMN {column}
            """
            self.db.cursor.execute(sql)
            self.db.commit_db()
            return True

        except sqlite3.OperationalError as err:
            return err
        

    ### Lista todas as colunas
    
    def table_info(self):
        try:
            sql = f"PRAGMA table_info({self.tb_name})"
            t = self.db.cursor.execute(sql)
            columns = [tupla[1] for tupla in t.fetchall()]
            return columns

        except sqlite3.OperationalError as err:
            return err
    
    ### Lista todas as tabelas
    
    def table_list(self):
        try:
            sql = """
            SELECT name FROM sqlite_master WHERE type='table' ORDER BY name
            """
            result = self.custom_selection(sql)

            if (result):

                tables = list()

                for table in result.fetchall():
                    tables.append(table[0])

                return tables

            else:
                return False

        except sqlite3.OperationalError as err:
            return err

    
    ### Visualiza o schema da tabela
    
    def table_schema(self):
        try:
            sql = "SELECT sql FROM sqlite_master WHERE type='table' AND name=?"
            schema = self.db.cursor.execute(sql, (self.tb_name,))
            return schema
        except sqlite3.OperationalError as err:
            return err

    
    ### Faz backup
    
    def do_backup(self, file_name="sql/tools.sql"):
        try:
            with io.open(file_name, "w") as f:
                for line in self.db.conn.iterdump():
                    f.write(f"{line}\n")
                    
            return True

        except sqlite3.OperationalError as err:
            return err

        
    ### Importa dados
    
    def import_data(self, db_name="banco.db" , file_name="sql/tools.sql"):
        try:
            self.db = Connect(db_name)
            f = io.open(file_name, 'r')
            sql = f.read()
            self.db.cursor.executescript(sql)
            return True

        except sqlite3.OperationalError as err:
            return err
