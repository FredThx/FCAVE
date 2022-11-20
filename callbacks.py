import logging
import dash
from dash.dependencies import Input, Output, State
from components.card_vin import CardVin
from app import app
from components.cave_bdd import Cave_Bdd
from components.cave import Cave

cave = Cave(Cave_Bdd('cave.db'), 'vins')

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

@app.callback(
    Output("dialogue_add", "is_open"),
    [
        Input("button_add_vin", "n_clicks"),
        Input("dialogue_add_vin_button_add", "n_clicks"),
    ],
    [
        State("dialogue_add", "is_open"),
        {id : State(id, 'value') for id in cave.get_input_ids('dialogue_add_vin')}, #Les champs de la boite de dialogue
    ]
)
def toggle_dialogue_add(n_open,n_add,is_open, values):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if  changed_id == "dialogue_add_vin_button_add.n_clicks":
        logging.debug(f"Ajout du vin. values = {values}")
        cave.bdd_insert('dialogue_add_vin', values)
    if n_open or n_add:
        return not is_open
    else:
        return is_open