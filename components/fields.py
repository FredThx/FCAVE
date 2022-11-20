from dash import html, dcc
import dash_bootstrap_components as dbc


class Field:
    """ Un champ de la base de données
    """

    def get_selecteur_id(self)->str:
        return f"option_{self.name}"
    
    @property
    def tooltip(self)->str:
        try:
            return self.placeholder
        except AttributeError:
            return ""

class FieldText(Field):
    """ Un champ de type texte
    """
    def __init__(self, field, table, name = None, placeholder = None):
        self.field = field
        self.table = table
        self.name = name or field
        self.placeholder = placeholder or self.name
        
    def get_selecteur(self)->html.Div:
        '''
        '''
        return html.Div([dcc.Dropdown(id = self.get_selecteur_id(), 
                            placeholder = f"Choix {self.name}",
                            multi = True),
                         dbc.Tooltip(dcc.Markdown(self.tooltip),
                                        placement = "top",
                                        class_name = "option-tooltip",
                                        delay = {'show': 50, 'hide': 50},
                                        target = self.get_selecteur_id())
                        ])
                        
    def get_choices(self, vins:list[dict])->list[str]:
        '''renvoie la liste des choix possibles
            vins    :   liste des vins resulats du filtrage
        '''
        choices = []
        for vin in vins:
            value = vin.get(self.field)
            if value and value not in choices:
                choices.append(value)
        return choices

class FieldTextList(FieldText):
    '''Un champ de type text avec liste d'option (ex : couleur = ['rouge', 'rosé','blanc'])
    '''
    def __init__(self, field, table, name = None, choices = None, placeholder = None):
        super().__init__(field, table, name = name, placeholder = placeholder)
        self.choices = choices or []
    
    def add_choice(self, choice):
        self.choices.append(choice)
    
class FieldTextForeign(FieldText):
    '''Un champ lié à une table ex : producteur
    '''
    def __init__(self, field, table, link_table, foreign_key = 'id', name=None, placeholder=None):
        super().__init__(field, table, name, placeholder)
        self.link_table = link_table
        self.foreign_key = foreign_key

