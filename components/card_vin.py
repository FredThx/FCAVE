import dash_bootstrap_components as dbc
from dash import html

class CardVin(dbc.Card):
    '''A bootstrap card for vins
    '''

    def __init__(self, vin):
        super().__init__(style={"width": "18rem"})
        self.vin = vin
        self.children = self.render()
    
    @property
    def data(self):
        return self.vin.__dict__

    def render(self):
        id = f"CardVin_{self.data['id']}" #juste pour tooltip
        return [
            dbc.CardHeader(html.H4(f"{self.data['name']} {self.data['millesime']}"), id = id),
            dbc.CardImg(src = "/static/images/fitou.jpg", top = True),
            #dbc.CardBody([html.P("todo")]),
            dbc.CardBody([
                html.H6(self.vin.appellation, className = "card-title"),
                html.P(f"Apogée entre {self.data['apogee_debut']} et {self.data['apogee_fin']}.", className = "card-text"),
                html.P(f"Stock : {self.data['stock']}", className = "card-text"),
                dbc.Row([
                    dbc.Col(dbc.Button("Details", color="primary", id = "id"+"_bt_edit")),
                    dbc.Col(dbc.Button("Supprime", color="primary", id = "id"+"_bt_remove")),
                ]),
            ]),
            dbc.Tooltip("todo : tooltip header", placement = "top", target= id)
            ]


