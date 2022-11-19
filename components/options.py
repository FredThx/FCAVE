from dash import html, dcc
import dash_bootstrap_components as dbc


class CaveOption:
    '''Une option (ex : couleur)
    '''
    def __init__(self, field, name, tooltip = None):
        self.field = field
        self.name = name
        self.tooltip = tooltip or name

    def get_selecteur(self):
        return html.Div([dcc.Dropdown(id = self.get_selecteur_id(), 
                            placeholder = f"Choix {self.name}",
                            multi = True),
                         dbc.Tooltip(dcc.Markdown(self.tooltip),
                                        placement = "top",
                                        class_name = "option-tooltip",
                                        delay = {'show': 50, 'hide': 50},
                                        target = self.get_selecteur_id())
                        ])
                        
    def get_selecteur_id(self):
        return f"option_{self.name}"


    def get_choices(self, vins:list[dict]):
        '''renvoie la liste des choix possibles
        vins    :   liste des vins resulats du tri
        '''
        choices = []
        for vin in vins:
            value = vin.get(self.field)
            if value and value not in choices:
                choices.append(value)
        return choices



class CaveOptionProps(CaveOption):
    '''Une option de type props
    '''
    pass