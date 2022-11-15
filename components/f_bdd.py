import sqlite3
import logging


class F_Bdd:
    '''Un classe pour accéder à une base de données sqlite3
    '''
    def __init__(self, bdd_file:str):
        self.conn = sqlite3.connect(bdd_file)
        self.conn.row_factory= sqlite3.Row
        self.structure = {} #pas sur que ce soit nécessaire

    def execute(self, req, values = None, commit = True):
        logging.debug(f'execute SQL : "{req}". VALUES = {values}')
        cursor = self.conn.cursor()
        try:
            if values : 
                cursor.execute(req, values)
            else:
                cursor.execute(req)
            if commit:
                self.conn.commit()
        except sqlite3.DatabaseError as e:
            logging.error(e)
        else:
            return [dict(r) for r in cursor.fetchall()]

    def create_tables(self, structure:dict):
        '''Create all the tables
        struct      :   a dict {'table_name' : {'field1' : attributs, ...}, ...}
                        attributs : str (ex : "TEXT")
        '''
        self.structure = structure
        for table, fields in self.structure.items():
            req = f"CREATE TABLE IF NOT EXISTS {table}("
            for field, attributes in fields.items():
                req += f"{field} {attributes}, "
            req = req[:-2] #Suppression du dernier ","
            req += ');'
            self.execute(req)

    def insert(self, table:str, records:list[dict]):
        '''Insert recorsd into a table
        records : {'field_name' : 'value"}
        '''
        if type(records)!=list:
            records = [records]
        for record in records:
            req = f"INSERT INTO {table} ({','.join(record.keys())}) VALUES ({','.join([':'+k for k in record.keys()])});"
            self.execute(req, record)
        
    def select(self, table:str, cols = None, where = None):
        '''Select from table
            table   :   table name
            cols    :   (optional) str or list of fields
            where   :   (optional) str or dict {'field' : value}
                        value can be a dict {'operator' : test_value}  (ex : {'$gt' : 42, '$lt' : 100}) )
        '''
        req = "SELECT "
        if cols is None:
            req += " * "
        elif type(cols) == str:
            req += f" {cols} "
        else:
            if type(cols)!=list:
                cols = [cols]
            req += ", ".join(cols)
        req += f" FROM {table}"
        if where:
            if type(where)==str:
                req += f" WHERE {where}"
            if type(where)==dict:
                req += " WHERE "+ " AND ".join([self.where(field, value) for field, value in where.items()])
        return self.execute(req)

    def where(self, field, values):
        if type(values) == list: #CLAUSE IN
            return f" {field} IN ({', '.join([self.str_value(value) for value in values])})"
        elif type(values) == dict: #CLAUSE GE, LE, GT, LT
            return " " + " AND ".join([f"{field} {self.clause_where(operator, value)}" for operator, value in values.items()])
        else:
            return f" {field}={self.str_value(values)} "

    operators = {
        '$gt' : '>',
        '$ge' : '>=',
        '$lt' : '<',
        '$le' : '<=',
        '$like' : 'LIKE'
    }

    def clause_where(self, operator:str, value):
        ''' A partir d'un couple operator, value, venvois la clause where correspondante.
        ex : clause_where('$gt", 42) return ">= 42"
        '''
        if operator in self.operators:
            return f"{self.operators[operator]} {self.str_value(value)}"
        else:
            raise Exception(f'Non valide operator : {operator}. Autorised values : {self.operators.keys()}.')

    @staticmethod
    def str_value(value):
        ''' Return "'value'" if str, else "value"
        '''
        if type(value)==str:
            return f'"{value}"'
        else:
            return str(value)