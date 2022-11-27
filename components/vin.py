from .card_vin import CardVin

class Vin:
    '''Un vin
    '''
    def __init__(self, bdd, **kwargs):
        self.bdd = bdd
        self.__dict__.update(kwargs)

    @property
    def appellation(self):
        '''Renvoie le nom de l'appellation
        '''
        if self.appellation_id:
            result = self.bdd.select('appellations', 'appellation_name', {'id' : self.appellation_id}, False)
            if result:
                return result[0]['appellation_name']
    
    @property
    def region(self):
        ''' Renvoie le nom de la région
        '''
        return "TODO!"

    def get(self, prop):
        return self.__dict__.get(prop)

    def get_card(self):
        return CardVin(self)
    