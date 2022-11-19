from dash import html, dcc
import dash_bootstrap_components as dbc

criteres = html.Div(id="criteres")

liste_des_vins = dbc.Row(id="liste_des_vins")

load_page = dcc.Interval(
    id = "load_page",
    n_intervals=0,
    max_intervals=0,
    interval=1
)

body = dbc.Container([
    dbc.Row([
        dbc.Col(criteres),
        dbc.Col(liste_des_vins)
        ]),
    load_page
])



layout_index =html.Div(body)
