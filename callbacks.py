import logging
from dash.dependencies import Input, Output, State
from app import app
from components.cave_bdd import Cave_Bdd
from components.cave import Cave

cave = Cave(Cave_Bdd('cave.db'))

@app.callback(
    [Output("liste_des_vins", "children")],
    [Input("liste_des_vins", "id")]
)
def update_liste_des_vins(_id):
    logging.debug("Callback update_liste_des_vins")
    liste_des_vins = cave.get_cards_vins()
    logging.debug(f"Liste_des_vins : {liste_des_vins}")
    return [liste_des_vins]
