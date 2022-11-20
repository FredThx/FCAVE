import logging

from .fields import Field, FieldText, FieldTextList, FieldTextForeign

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
        FieldText("name", table = 'vins', name = "Nom", placeholder = "Nom du vin"),
        FieldTextList("color", table = 'vins', name = "Couleur", placeholder = "Couleur du vin"),
        FieldTextForeign("region_name", table = "regions", link_table = 'appellations', name ="Région"),
        FieldTextForeign("appellation_name", table = "appellations", link_table = 'vins', name = "Appellation"),
        FieldTextForeign("producer_name", table = "producers", link_table = 'vins', name = "Producteur"),
    ]#TODO : sortir ça d'ici avec :

    def add_options(self, options:list[Field]):
        if type(options)!=list:
            options = [options]
        self.options += options

    def get_selecteurs(self):
        '''Renvoie la liste des selecteurs (options)
        '''
        return [option.get_selecteur() for option in self.options]
    
    def get_selecteurs_id(self):
        return [option.get_selecteur_id() for option in self.options]

    fields = {

    }