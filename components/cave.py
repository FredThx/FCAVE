import logging
from .card_vin import CardVin

class Cave():
    '''Une application de gestion de cave
    '''
    def __init__(self, bdd):
        self.bdd = bdd
    
    def get_vins(self):
        logging.debug(f"get_vins()...")
        vins = self.bdd.select('vins')
        logging.debug(f"get_vins():{vins}")
        return vins

    def get_cards_vins(self, *args, **kwargs):
        return [CardVin(vin) for vin in self.get_vins(*args, **kwargs)]