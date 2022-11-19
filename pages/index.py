from dash import html
import dash_bootstrap_components as dbc

criteres = "Critères"
liste_des_vins = dbc.Row(id="liste_des_vins")


body = dbc.Container([
    dbc.Row([
        dbc.Col(criteres),
        dbc.Col(liste_des_vins)
        ])
])



layout_index =html.Div(body)
