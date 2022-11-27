import logging
import dash
from dash.dependencies import Input, Output, State
from components.card_vin import CardVin
from app import app
from components.cave_bdd import Cave_Bdd
from components.cave import Cave
from components.dash_utils import change_props

cave = Cave(Cave_Bdd('cave.db'), 'vins')

@app.callback(
    [
        Output("liste_des_vins", "children"),
        [Output(id, 'options') for id in cave.get_selecteurs_id()]
    ],
    [
        {id : Input(id, 'value') for id in cave.get_selecteurs_id()},
        Input("load_page","n_clicks"),
        Input("switch_collapse_on_off", "value"),
    ],
    [
        State("liste_des_vins", "children"),
        [State(id, 'options') for id in cave.get_selecteurs_id()]
    ]

)
def update_liste_des_vins(options, load_page, switch_collapse_on_off, liste_des_vins, options_values):
    options = options
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    logging.debug(f"Callback update_liste_des_vins. changed_id = {changed_id}. options = {options},  switch_collapse_on_off = {switch_collapse_on_off}")
    if liste_des_vins and changed_id == "switch_collapse_on_off.value":
        change_props(liste_des_vins, r"CardVin_\d+_collapse", "is_open", switch_collapse_on_off)
    else:
        vins = cave.get_vins(options)
        liste_des_vins = [CardVin(vin, not switch_collapse_on_off) for vin in vins]
        options_values = [option.get_choices(vins) for option in cave.options]
    #logging.debug(f"Liste_des_vins : {liste_des_vins}")
    return [liste_des_vins, options_values]

@app.callback(
    [
        Output("dialogue_add", "is_open"),
        Output('load_page', "n_clicks"),
        [Output(id, 'value') for id in cave.get_input_ids('dialogue_add_vin')], #Les champs de la boite de dialogue
    ],
    [
        Input("button_add_vin", "n_clicks"),
        Input("dialogue_add_vin_button_add", "n_clicks"),
    ],
    [
        State("dialogue_add", "is_open"),
        State("load_page", "n_clicks"),
        {id : State(id, 'value') for id in cave.get_input_ids('dialogue_add_vin')}, #Les champs de la boite de dialogue
    ]
)
def toggle_dialogue_add(n_open, n_add, is_open, load_page_n_clicks, values):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if  changed_id == "dialogue_add_vin_button_add.n_clicks":
        logging.debug(f"Ajout du vin. values = {values}")
        cave.bdd_insert('dialogue_add_vin', values)
        load_page_n_clicks = load_page_n_clicks or + 1 #Pour recharger la liste des vins
    if n_open or n_add:
        return [not is_open, load_page_n_clicks, [None for id in cave.get_input_ids('dialogue_add_vin')]]
    else:
        return [is_open, load_page_n_clicks, [None for id in cave.get_input_ids('dialogue_add_vin')]]

