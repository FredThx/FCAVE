from .card_vin import CardVin
from unidecode import unidecode

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
        if self.get('appellation_id'):
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

    def get_card(self, collapse = False):
        return CardVin(self, collapse)

    def match_text(self, text):
        '''Return true if the searched text is in props
        '''
        text = unidecode(text).casefold()
        for prop in self.__dict__:
            if prop not in ['bdd', 'id']:
                if type(self.get(prop))==str and text in unidecode(self.get(prop)).casefold():
                    return True
        return False

    