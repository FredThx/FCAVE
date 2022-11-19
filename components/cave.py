import logging

from .options import CaveOption

class Cave():
    '''Une application de gestion de cave
    '''
    def __init__(self, bdd):
        self.bdd = bdd
    
    def get_vins(self, options = None):
        logging.debug(f"get_vins()...")
        vins = self.bdd.select('vins')
        logging.debug(f"get_vins():{vins}")
        return vins

    def get_cards_vins(self, *args, **kwargs):
        return [CardVin(vin) for vin in self.get_vins(*args, **kwargs)]
    
    options = [
        CaveOption("color", "Couleur", "Couleur du vin"),
        CaveOption("region_name", "Région"),
        CaveOption("appellation_name", "Appellation"),
        CaveOption("producer_name", "Producteur"),
    ]

    def get_selecteurs(self):
        '''Renvoie la liste des selecteurs (options)
        '''
        return [option.get_selecteur() for option in self.options]
    
    def get_selecteurs_id(self):
        return [option.get_selecteur_id() for option in self.options]