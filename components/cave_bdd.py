from f_bdd import *

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
            'notes' : 'TEXT'
        },
        'producers' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'name' : 'TEXT',
            'address' : 'TEXT',
            'notes' : 'TEXT'
        },
        'appelations' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'name' : 'TEXT',
            'region_id' : 'INTEGER'
        },
        'regions' : {
            'id' : 'INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE',
            'name' : 'TEXT'
        }
    }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.create_tables(self.struct)


if __name__ == '__main__':
    from FUTIL.my_logging import *
    my_logging(console_level = DEBUG, logfile_level = INFO, details = True)

    bdd = Cave_Bdd('ma_base.db')
    #print(bdd.execute("SELECT * FROM sqlite_master;"))
    #bdd.insert('vins',[{'name' : 'nom du vin', 'color' : 'Rouge'}, {'name' : 'un vin blanc', 'color' : 'Blanc'}])
    print(bdd.select('vins',['id', 'name', 'color'], {'color' : ['Rouge','Blanc']}))
    print(bdd.select('vins',['id', 'name', 'color'], {'color' : {'$like' : 'R%'}}))
