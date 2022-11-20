import logging
import dash_bootstrap_components as dbc

from .fields import Field, FieldText, FieldTextList, FieldTextForeign, FieldInteger
from .card_vin import CardVin


class Cave():
    '''Une application de gestion de cave
    '''
    def __init__(self, bdd):
        self.bdd = bdd
        self.options =  []
        self.fields = []
        #TODO : mettre ça ailleurs (et donc renommer la classe en un truc de générique)
        f_name = FieldText("name", table = 'vins', name = "Nom", placeholder = "Nom du vin")
        f_color = FieldTextList("color", table = 'vins', name = "Couleur", placeholder = "Couleur du vin", values = ["rouge","blanc", "rosé"])
        f_region = FieldTextForeign("region_name", table = "regions", link_table = 'appellations', name ="Région")
        f_appellation = FieldTextForeign("appellation_name", table = "appellations", link_table = 'vins', name = "Appellation")
        f_producer = FieldTextForeign("producer_name", table = "producers", link_table = 'vins', name = "Producteur")
        f_props = FieldText("props", table = 'vins', name = "Propriétes", placeholder = "Propriétés de ce vin (ex : sec/doux, ...)")
        f_millesime = FieldInteger("millesime", table = 'vins', name = "Millésime", min = 1900, max = 3000)
        self.add_options([f_name, f_color, f_region, f_appellation, f_producer])
        self.add_fields([f_name, f_millesime, f_color, f_appellation, f_producer, f_props])

    def add_options(self, options:list[Field]):
        if type(options)!=list:
            options = [options]
        self.options += options
    
    def add_fields(self, fields:list[Field]):
        if type(fields)!=list:
            fields = [fields]
        self.fields += fields

    def get_vins(self, options = None):
        logging.debug(f"get_vins()...")
        vins = self.bdd.select('vins')
        logging.debug(f"get_vins():{vins}")
        return vins

    def get_cards_vins(self, *args, **kwargs):
        return [CardVin(vin) for vin in self.get_vins(*args, **kwargs)]

    def get_selecteurs(self):
        '''Renvoie la liste des selecteurs (options)
        '''
        return [option.get_selecteur() for option in self.options]
    
    def get_selecteurs_id(self):
        return [option.get_selecteur_id() for option in self.options]

    def get_input_groups(self, root_id = "")->list[dbc.InputGroup]:
        return [field.get_input_group(root_id) for field in self.fields]
