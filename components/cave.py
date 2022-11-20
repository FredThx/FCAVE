import logging

from .fields import Field, FieldText, FieldTextList, FieldTextForeign

class Cave():
    '''Une application de gestion de cave
    '''
    def __init__(self, bdd):
        self.bdd = bdd
        self.options =  []
        #TODO : mettre ça ailleurs (et donc renommer la classe en un truc de générique)
        f_name = FieldText("name", table = 'vins', name = "Nom", placeholder = "Nom du vin")
        f_color = FieldTextList("color", table = 'vins', name = "Couleur", placeholder = "Couleur du vin")
        f_region = FieldTextForeign("region_name", table = "regions", link_table = 'appellations', name ="Région")
        f_appellation = FieldTextForeign("appellation_name", table = "appellations", link_table = 'vins', name = "Appellation")
        f_producer = FieldTextForeign("producer_name", table = "producers", link_table = 'vins', name = "Producteur")
        self.add_options([f_name, f_color, f_region, f_appellation, f_producer])

    def get_vins(self, options = None):
        logging.debug(f"get_vins()...")
        vins = self.bdd.select('vins')
        logging.debug(f"get_vins():{vins}")
        return vins

    def get_cards_vins(self, *args, **kwargs):
        return [CardVin(vin) for vin in self.get_vins(*args, **kwargs)]
    
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