import logging
import dash_bootstrap_components as dbc

from .fields import Field, FieldText, FieldTextList, FieldTextForeign, FieldInteger, FieldRange, FieldtextArea, FieldFloat
from .card_vin import CardVin


class Cave():
    '''Une application de gestion de cave
    '''
    def __init__(self, bdd):
        self.bdd = bdd
        self.options =  []
        self.fields = []
        #TODO : mettre ça ailleurs (et donc renommer la classe en un truc de générique)
        f_name = FieldText(bdd, "name", table = 'vins', name = "Nom", placeholder = "Nom du vin")
        f_color = FieldTextList(bdd, "color", table = 'vins', name = "Couleur", placeholder = "Couleur du vin", values = ["rouge","blanc", "rosé"])
        f_region = FieldTextForeign(bdd, "region_name", table = "regions", linked_table = 'appellations', name ="Région")
        f_appellation = FieldTextForeign(bdd, "appellation_name", table = "appellations", linked_table = 'vins', name = "Appellation")
        f_producer = FieldTextForeign(bdd, "producer_name", table = "producers", linked_table = 'vins', name = "Producteur")
        f_props = FieldText(bdd, "props", table = 'vins', name = "Propriétes", placeholder = "Propriétés de ce vin (ex : sec/doux, ...)")
        f_millesime = FieldInteger(bdd, "millesime", table = 'vins', name = "Millésime", min = 1900, max = 3000)
        f_apogee_debut = FieldInteger(bdd, "apogee_debut", table = 'vins', name = "Apogée début", min = 1900, max = 3000)
        f_apogee_fin = FieldInteger(bdd, "apogee_fin", table = 'vins', name = "Apogée fin", min = 1900, max = 3000)
        f_apogee =FieldRange(bdd, f_apogee_debut, f_apogee_fin, name = "Apogée")
        f_notes = FieldtextArea(bdd, "notes", table = 'vins', name = "Notes", placeholder = "Notes (ex: 'Super bon vin!')")
        f_stock = FieldInteger(bdd, "stock", table = 'vins', name = "Stock", min = 0)
        f_price = FieldFloat(bdd, "price", table = 'vins', name = "Prix unitaire", min = 0, unit = "€")
        self.add_options([f_name, f_color, f_region, f_appellation, f_producer])
        self.add_fields([f_name, f_millesime, f_color, f_appellation, f_producer, f_props, f_apogee, f_notes, f_stock, f_price])

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
