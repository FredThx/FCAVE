import sqlite3
import logging

#TODO:
# Pour simplifier les jointures automatiques,
# actuellement, il faut des noms de champs duistincts entre les != tables (ex name de producers = producer_name)
# Soit
#   - lors de la création de la base, interdir les champs commun
#   - ne pas utiliser de select *, mais 

class F_Bdd:
    '''Un classe pour accéder à une base de données sqlite3
    '''
    def __init__(self, bdd_file:str):
        self.bdd_file = bdd_file
        self.structure = {}
        self.execute("PRAGMA foreign_keys = ON;")

    def get_conn(self):
        conn = sqlite3.connect(self.bdd_file)
        conn.row_factory= sqlite3.Row
        return conn

    def execute(self, req, values = None, commit = True, return_count = False):
        logging.debug(f'execute SQL : "{req}". VALUES = {values}')
        conn = self.get_conn()
        cursor = conn.cursor()
        try:
            if values :
                #if type(values) not in [list, tuple, dict]:
                #    values = (values,)
                cursor.execute(req, values)
            else:
                cursor.execute(req)
            if commit:
                conn.commit()
        except sqlite3.DatabaseError as e:
            logging.error(e)
        else:
            if return_count:
                return cursor.rowcount
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
                if field[:2]!='__':
                    req += f"{field} {attributes}, "
                elif field == '__foreign_key__':
                    if type(attributes) not in [list, tuple]:
                        attributes = [attributes]
                        self.structure[table]['__foreign_key__'] = attributes
                    for attribute in attributes:
                        try:
                            req += f"FOREIGN KEY({attribute['key']}) REFERENCES {attribute['table']}({attribute['foreign_key']}), "
                        except KeyError as e:
                            logging.error(e)
            req = req[:-2] #Suppression du dernier ","
            req += ');'
            self.execute(req)

    def insert(self, table:str, records:list[dict]):
        '''Insert recorsd into a table
        records : {'field_name' : 'value"}
        '''#TODO : renvoyer les enregistrements inserés (faire un select ou ...)
        if type(records)!=list:
            records = [records]
        for record in records:
            req = f"INSERT INTO {table} ({','.join(record.keys())}) VALUES ({','.join([':'+k for k in record.keys()])});"
            self.execute(req, record)
        
    def delete(self, table:str, ids, id_field="id"):
        '''Delete row(s) on table, 
        ids     :   integer or list of integer or dict (with id_field key) or list of dict
        exemples : 
            self.delete('ma_table', 42)
            self.delete('ma_table', (5,6,9))
            self.delete('ma_table', self.select('ma_table',where={'col1' : 42}))
        '''
        if type(ids) not in (tuple, list):
            ids = [ids]
        req = f"DELETE FROM {table} WHERE {id_field} IN ({','.join('?' * len(ids))})"
        try:
            ids = [id[id_field] if type(id)==dict else id for id in ids]
        except KeyError as e:
            logging.error(e)
            return 0
        return self.execute(req, ids, return_count=True)



    def select(self, table:str, cols = None, where = None, foreign = True):
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
        if foreign:
            for jointure in self.jointures(table):
                req += f" {jointure.get('join','INNER JOIN')} {jointure['table']} ON {jointure['table']}.{jointure['foreign_key']} = {jointure['table_A']}.{jointure['key']}"
        if where:
            if type(where)==str:
                req += f" WHERE {where}"
            if type(where)==dict:
                req += " WHERE "+ " AND ".join([self.where(table, field, value) for field, value in where.items()])
        return self.execute(req)

    def jointures(self, table)->list[dict]:
        '''Return the list of jointure from structure
        '''
        jointures = []
        for foreign_key in self.structure[table].get('__foreign_key__', []):
            foreign_key['table_A']=table
            jointures.append(foreign_key)
            jointures+=(self.jointures(foreign_key['table']))
        return jointures

    def where(self, table, field, values)->str:
        if field in self.structure.get(table):
            field = f"{table}.{field}"
        else:
            for jointure in self.jointures(table):
                if field in self.structure.get(jointure['table']):
                    field = f"{jointure['table']}.{field}"
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

    def clause_where(self, operator:str, value)->str:
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