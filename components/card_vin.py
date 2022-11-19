import dash_bootstrap_components as dbc
from dash import html

class CardVin(dbc.Card):
    '''A bootstrap card for vins
    '''

    def __init__(self, vin:dict):
        #TODO : on verra s'il faut passer des object Vin et non pas des dict
        super().__init__(style={"width": "18rem"})
        self.data = vin
        self.children = self.render()

    def render(self):
        id = f"CardVin_{self.data['id']}" #juste pour tooltip
        return [
            dbc.CardHeader(self.data['name'], id = id),
            dbc.CardImg(src = "todo", top = True),
            #dbc.CardBody([html.P("todo")]),
            dbc.CardBody([html.P([f"{k} : {v}" for k, v in self.data.items()])]),
            dbc.Tooltip("todo : tooltip header", placement = "top", target= id)
            ]


