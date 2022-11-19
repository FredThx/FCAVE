import logging
from dash.dependencies import Input, Output, State
from components.card_vin import CardVin
from app import app
from components.cave_bdd import Cave_Bdd
from components.cave import Cave

cave = Cave(Cave_Bdd('cave.db'))

@app.callback(
    [Output("criteres", "children")],
    [Input("load_page", "n_intervals")]
)
def update_criteres(n_intervals):
    return [cave.get_selecteurs()]


@app.callback(
    [
        Output("liste_des_vins", "children"),
        [Output(id, 'options') for id in cave.get_selecteurs_id()]
    ],
    inputs = dict(
        options = {id : Input(id, 'value') for id in cave.get_selecteurs_id()}
    )
)
def update_liste_des_vins(options):
    logging.debug("Callback update_liste_des_vins")
    vins = cave.get_vins(options)
    liste_des_vins = [CardVin(vin) for vin in vins]
    options_values = [option.get_choices(vins) for option in cave.options]
    logging.debug(f"Liste_des_vins : {liste_des_vins}")
    return [liste_des_vins, options_values]

