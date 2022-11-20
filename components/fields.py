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
    
    def input_id(self, root_id):
        return f"{root_id}_{self.name}"

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
    
    def get_input_group(self, root_id = "")->dbc.InputGroup:
        return dbc.InputGroup(
            [dbc.InputGroupText(self.name), dbc.Input(id = self.input_id(root_id), placeholder=self.placeholder)],
            className="mb-3")

class FieldTextList(FieldText):
    '''Un champ de type text avec liste d'option (ex : couleur = ['rouge', 'rosé','blanc'])
    '''
    def __init__(self, field, table, name = None, values = None, placeholder = None):
        super().__init__(field, table, name = name, placeholder = placeholder)
        self.values = values or []
    
    def add_choice(self, choice):
        self.choices.append(choice)

    def get_input_group(self, root_id = "")->dbc.InputGroup:
        return dbc.InputGroup(
                    [   dbc.InputGroupText(self.name),
                        dbc.Select(
                            options = [{"label" : value.capitalize(), "value" : value} for value in self.values],
                            id = self.input_id(root_id))])
    
class FieldTextForeign(FieldText):
    '''Un champ lié à une table ex : producteur
    '''
    def __init__(self, field, table, link_table, foreign_key = 'id', name=None, placeholder=None):
        super().__init__(field, table, name, placeholder)
        self.link_table = link_table
        self.foreign_key = foreign_key

class FieldInteger(FieldText):
    '''Un champ Integer
    '''
    def __init__(self, field, table, name=None, placeholder=None, min = None, max = None, step = 1):
        super().__init__(field, table, name, placeholder)
        self.min = min
        self.max = max
        self.step = step

    def get_input_group(self, root_id = "")->dbc.InputGroup:
        return dbc.InputGroup(
            [   dbc.InputGroupText(self.name),
                dbc.Input(
                    type = "number", min = self.min, max = self.max, step = self.step,
                    id = self.input_id(root_id), placeholder=self.placeholder)],
            className="mb-3")