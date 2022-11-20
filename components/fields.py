from dash import html, dcc
import dash_bootstrap_components as dbc
from components.cave_bdd import Cave_Bdd


class Field:
    """ Un champ de la base de données
    """

    def __init__(self, bdd:Cave_Bdd, name:str) -> None:
        self.bdd = bdd
        self.name = name

    def get_selecteur_id(self)->str:
        return f"option_{self.name}"
    
    def get_fields(self):
        return [self]

    @property
    def tooltip(self)->str:
        try:
            return self.placeholder
        except AttributeError:
            return ""
    
    def input_id(self, root_id:str)->str:
        return f"{root_id}_{self.name}"

    def get_input_group(self, root_id:str = "")->dbc.InputGroup:
        ''' Renvoie la représentation dbc du champ pour intégration en html
        '''
        return dbc.InputGroup(
            [   dbc.InputGroupText(self.name),
                self.get_input(root_id),
            ],
            className="mb-3")

class FieldText(Field):
    """ Un champ de type texte
    """
    def __init__(self, bdd:Cave_Bdd, field:str, table:str, name:str = None, placeholder:str = None) -> None:
        super().__init__(bdd, name or field)
        self.field = field
        self.table = table
        self.placeholder = placeholder or self.name

    def input_id(self, root_id:str)->str:
        return f"{root_id}_{self.field}"

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

    def get_input(self, root_id:str = "")->dbc.Input:
        """ Renvoie juste la zone de saisie du champ
        """
        return dbc.Input(id = self.input_id(root_id), placeholder=self.placeholder)

class FieldtextArea(FieldText):
    ''' Un champ TEXT large
    '''
    def get_input(self, root_id:str = "")->dbc.Textarea:
        """ Renvoie juste la zone de saisie du champ
        """
        return dbc.Textarea(id = self.input_id(root_id), placeholder=self.placeholder)  


class FieldTextList(FieldText):
    '''Un champ de type text avec liste d'option (ex : couleur = ['rouge', 'rosé','blanc'])
    '''
    def __init__(self, bdd:Cave_Bdd, field:str, table:str, name:str = None, values:list[str] = None, placeholder:str = None)->None:
        super().__init__(bdd, field, table, name = name, placeholder = placeholder)
        self.values = values or []

    def get_input(self, root_id:str = "")->dbc.Select:
        """ Renvoie juste la zone de saisie du champ
        """
        return dbc.Select(
                    options = [{"label" : value.capitalize(), "value" : value} for value in self.values],
                    id = self.input_id(root_id))
    
class FieldTextForeign(FieldText):
    '''Un champ lié à une table ex : producteur
    '''
    def __init__(self, bdd:Cave_Bdd, field:str, table:str, linked_table:str, foreign_field:str = None, foreign_key:str = 'id', name:str=None, placeholder:str=None):
        super().__init__(bdd, field, table, name, placeholder)
        self.foreign_field = foreign_field or f"{self.table[-1]}_id"
        self.linked_table = linked_table
        self.foreign_key = foreign_key

    
    def get_input(self, root_id:str = "") -> dbc.Select:
        return dbc.Select(
                    options = [{"label" : row.get(self.name), "value" : row.get(self.foreign_key)} for row in self.get_foreign()]
                            + [{"label" : f"<Nouveau {self.name}", "value" : "new"}],
                    id = self.input_id(root_id))
    
    def get_foreign(self)->list[dict]:
        '''renvoie la liste des enregistrements de la table foreign
        '''
        return self.bdd.select(self.table)


class FieldInteger(FieldText):
    '''Un champ Integer
    '''
    def __init__(self, bdd:Cave_Bdd, field:str, table:str, name:str=None, placeholder:str=None, min:int = None, max:int = None, step:int = 1):
        super().__init__(bdd, field, table, name, placeholder)
        self.min = min
        self.max = max
        self.step = step
    
    def get_input(self, root_id:str = "")->dbc.Input:
        return dbc.Input(
                    type = "number", min = self.min, max = self.max, step = self.step,
                    id = self.input_id(root_id), placeholder=self.placeholder)

class FieldFloat(FieldInteger):
    '''Un champ Float (avec unité)
    '''
    def __init__(self, bdd: Cave_Bdd, field: str, table: str, name: str = None, placeholder: str = None, min: int = None, max: int = None, step: int = 1, unit:str=None):
        super().__init__(bdd, field, table, name, placeholder, min, max, step)
        self.unit = unit
        self.step = 0.1 #Bug de dbc : si step est entier (même 1.0) => impossible de saisir des float

    def get_input_group(self, root_id: str = "") -> dbc.InputGroup:
        group = super().get_input_group(root_id)
        group.children.insert(1,dbc.InputGroupText(self.unit))
        return group

class FieldRange(Field):
    ''' Un champ plage (debut-fin) (ex : apogée)
        En fait ce sont deux champs qui s'affichent l'un a coté de l'autre
    '''
    def __init__(self, bdd:Cave_Bdd, field_min:Field, field_max:Field, name:str=None)->None:
        name = name or f"{field_min.name}-{field_max.name}"
        super().__init__(bdd, name)
        self.field_min = field_min
        self.field_max = field_max
    
    def get_fields(self):
        return [self.field_min, self.field_max]

    def get_input_group(self, root_id = "")-> dbc.InputGroup:
        return dbc.InputGroup(
            [
                dbc.InputGroupText(self.name),
                self.field_min.get_input(root_id),
                self.field_max.get_input(root_id)
            ], className = "mb-3"
            )
    get_input = get_input_group
    
    def input_id(self, root_id: str) -> list:
        return [self.field_min.input_id(root_id), self.field_max.input_id(root_id)]