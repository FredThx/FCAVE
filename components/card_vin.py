import dash_bootstrap_components as dbc
from dash import html

class CardVin(dbc.Card):
    '''A bootstrap card for vins
    '''
    colors = {
        'rouge' : 
        {
            'color' : '#47226A',
            'inverse' : True,
        },
        'blanc' : 
        {
            'color' : '#EDEAA5',
        },
        'rosé' : 
        {
            'color' : '#E1A7D2',
        },
        None :
        {
            'color' : "grey"
        }
            }
    def __init__(self, vin):
        super().__init__(style={"width": "18rem"})
        self.vin = vin
        self.children = self.render()
        self.className = "w-25 mx-1 my-1"
        for attr_color, value in self.colors.get(vin.color).items():
            self.__setattr__(attr_color, value)
    
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
                html.P(f"Apogée entre {self.data['apogee_debut'] or '___'} et {self.data['apogee_fin'] or '___'}.", className = "card-text"),
                html.P(f"Stock : {self.data['stock'] or 0}", className = "card-text"),
            ]),
            dbc.CardFooter(
                dbc.Row([
                    dbc.Col(dbc.Button("Details", color="primary", id = "id"+"_bt_edit"), width = 5),
                    dbc.Col(dbc.Button("Supprime", color="primary", id = "id"+"_bt_remove"), width =5),
                ]),
            ),
            dbc.Tooltip("todo : tooltip header", placement = "top", target= id)
            ]


