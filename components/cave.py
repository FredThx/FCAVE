import logging
import dash_bootstrap_components as dbc

from .field import Field, FieldText, FieldTextList, FieldTextForeign, FieldInteger, FieldRange, FieldtextArea, FieldFloat
from .vin import Vin


class Cave():
    '''Une application de gestion de cave
    '''
    def __init__(self, bdd, table):
        self.bdd = bdd
        self.table = table
        self.options =  []
        self.fields = []
        self._actives_cards_vins = {} # {'card_id' : vin}
        #TODO : mettre ça ailleurs (et donc renommer la classe en un truc de générique)
        f_name = FieldText(bdd, "name", table = 'vins', name = "Nom", placeholder = "Nom du vin")
        f_color = FieldTextList(bdd, "color", table = 'vins', name = "Couleur", placeholder = "Couleur du vin", values = ["rouge","blanc", "rosé"])
        f_region = FieldTextForeign(bdd, "region_name", table = "regions", linked_table = 'appellations', foreign_field = 'region_id', name ="Région")
        f_appellation = FieldTextForeign(bdd, "appellation_name", table = "appellations", linked_table = 'vins', foreign_field = 'appellation_id',name = "Appellation")
        f_producer = FieldTextForeign(bdd, "producer_name", table = "producers", linked_table = 'vins', foreign_field = 'producer_id', name = "Producteur")
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

    def get_vins(self, options = None, text_search:str = None)->list[dict]:
        '''Renvoie la liste des vins qui correspondent aux oprtions et texte de recherche
        '''
        #logging.debug(f"get_vins()...")
        filter = {}
        for field in self.options:
            option = options.get(field.get_selecteur_id())
            if option:
                filter[field.field] = option
        vins = [Vin(self.bdd,**data) for data in self.bdd.select('vins', where = filter)]
        if text_search:
            vins = [vin for vin in vins if vin.match_text(text_search)]
        #logging.debug(f"get_vins():{vins}")
        return vins or []

    def get_cards_vins(self, collapse = False, *args, **kwargs):
        '''Renvoie la liste des vins sous forme de CardVin
        et met en cache un dict {'card_id' : vin}
        '''
        cards = [vin.get_card(collapse) for vin in self.get_vins(*args, **kwargs)]
        self._actives_cards_vins = {card.id : card.vin for card in cards} 
        return cards
    
    @property
    def actives_vins(self)->list[Vin]:
        ''' Renvoie la liste des vins actifs
        '''
        return [vin for id,vin in self._actives_cards_vins.items()]

    def get_active_vin_by_card_id(self, card_id:str)->Vin:
        return self._actives_cards_vins[card_id]

    def get_selecteurs(self):
        '''Renvoie la liste des selecteurs (options)
        '''
        return [option.get_selecteur() for option in self.options]
    
    def get_selecteurs_id(self):
        return [option.get_selecteur_id() for option in self.options]

    def get_input_groups(self, root_id = "")->list[dbc.InputGroup]:
        return [field.get_input_group(root_id) for field in self.fields]
    
    def get_fields(self)->list[Field]:
        '''renvoie la liste des champs réels (ie pour les FieldRange : les 2 champs)
        '''
        return [field for fields in [field.get_fields() for field in self.fields] for field in fields]

    def get_input_ids(self, root_id:str)->list[str]:
        return [field.input_id(root_id) for field in self.get_fields()]
    
    def get_input_values(self, vin: Vin)->list:
        return [vin.__getattribute__(field.field) for field in self.get_fields()]

    def bdd_insert(self, root_id, data:dict)->None:
        '''Insert un nouvel enregistrement
        data : {'input_id' : 'valeur saisie'}
        '''
        values_to_insert = {}
        for field in self.get_fields():
            if data[field.input_id(root_id)] is not None:
                if field.table == self.table:
                    values_to_insert[field.field]=data[field.input_id(root_id)]
                else:
                    values_to_insert[field.foreign_field]=data[field.input_id(root_id)]
        logging.debug(f"bdd_insert : {values_to_insert}")
        self.bdd.insert(self.table, values_to_insert)
        