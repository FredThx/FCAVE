try:
    from .f_bdd import F_Bdd
except:
    from f_bdd import F_Bdd

class Cave_Bdd(F_Bdd):
    '''Une dase de donnée (sqlite3) pour stockage données cave
    '''
    struct = {
        'vins' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'name' : 'TEXT',
            'producer_id' : 'INTEGER',
            'appellation_id' : 'INTEGER',
            'color' : "TEXT CHECK( color IN ('Rouge', 'Blanc', 'Rosé'))",
            'props' : "TEXT",
            'millesime' : "INTEGER",
            'apogee_debut' : 'TIMESTAMP',
            'apogee_fin' : 'TIMESTAMP',
            'notes' : 'TEXT',
            '__foreign_key__' : [
                        {'key' : 'producer_id', 'table' : 'producers','foreign_key' : 'id'},
                        {'key' : 'appellation_id', 'table' : 'appellations','foreign_key' : 'id'}]
        },
        'producers' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'producer_name' : 'TEXT',
            'producer_address' : 'TEXT',
            'producer_notes' : 'TEXT'
        },
        'appellations' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'appellation_name' : 'TEXT',
            'region_id' : 'INTEGER',
            '__foreign_key__' : {'key' : 'region_id', 'table' : 'regions','foreign_key' : 'id'},
        },
        'regions' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'region_name' : 'TEXT'
        }
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_tables(self.struct)


if __name__ == '__main__':
    from FUTIL.my_logging import *
    my_logging(console_level = DEBUG, logfile_level = INFO, details = True)
    bdd = Cave_Bdd('cave.db')
    #print(bdd.execute("SELECT * FROM sqlite_master;"))
    bordeaux = {'region_name' : 'Bordeaux'}
    bdd.insert('regions',bordeaux)
    bordeaux = bdd.select('regions','*', bordeaux)[0]
    margaux = {'appellation_name' : "Margaux", 'region_id' : bordeaux['id']}
    bdd.insert('appellations',margaux)
    margaux = bdd.select('appellations','*', margaux)[0]
    toto = {'producer_name' : 'Toto'}
    bdd.insert('producers',toto)
    toto = bdd.select('producers',None ,toto)[0]
    bdd.insert('vins',[{'name' : 'Super Vin', 'color' : 'Rouge', 'producer_id' : toto['id'], 'appellation_id' : margaux['id']}, {'name' : 'un vin blanc', 'color' : 'Blanc', 'producer_id' : 42}])
    print(bdd.select('vins',['id', 'name', 'color'], {'color' : ['Rouge','Blanc']}))
    #print(bdd.select('vins',['id', 'name', 'color'], {'color' : {'$like' : 'R%'}}))
    print(f"Nb de vins suprimés : {bdd.delete('vins',bdd.select('vins',['id', 'name', 'color'], {'color' : 'Blanc'}))}")
    print(bdd.select('vins'))