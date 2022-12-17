import logging, re
import dash
from dash.dependencies import Input, Output, State
from components.card_vin import CardVin
from app import app
from components.cave_bdd import Cave_Bdd
from components.cave import Cave
from components.dash_utils import change_props

cave = Cave(Cave_Bdd('cave.db'), 'vins')

n_clicks = {}

@app.callback(
    [
        Output("liste_des_vins", "children"),
        [Output(id, 'options') for id in cave.get_selecteurs_id()]
    ],
    [
        {id : Input(id, 'value') for id in cave.get_selecteurs_id()},
        Input("load_page","n_clicks"),
        Input("text_search", "value"),
        Input("switch_collapse_on_off", "value"),
        Input({'type': 'dynamic_bt_collapse', 'index': dash.ALL}, 'value'),
    ],
    [
        State("liste_des_vins", "children"),
        [State(id, 'options') for id in cave.get_selecteurs_id()],
        State({'type': 'dynamic_bt_collapse', 'index': dash.ALL}, 'id'),
    ]

)
def update_liste_des_vins(options, load_page, text_search, switch_collapse_on_off, dynamic_bt_collapse_value, liste_des_vins, options_values, dynamic_bt_collapse_id):
    options = options
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    logging.debug(f"Callback update_liste_des_vins. changed_id = {changed_id}. options = {options},  switch_collapse_on_off = {switch_collapse_on_off}")
    if liste_des_vins and changed_id == "switch_collapse_on_off.value":
        change_props(liste_des_vins, r"CardVin_\d+_collapse", "is_open", switch_collapse_on_off)
        change_props(liste_des_vins, {'index' : r"CardVin_\d+_collapse"}, "value", switch_collapse_on_off)
    elif liste_des_vins and re.match('{"index":"CardVin_\d+_collapse","type":"dynamic_bt_collapse"}.value', changed_id):
        bt_id = re.search(r"CardVin_\d+_collapse", changed_id).group(0)
        index = [x['index'] for x in dynamic_bt_collapse_id].index(bt_id)
        change_props(liste_des_vins, bt_id, "is_open", dynamic_bt_collapse_value[index])
    else:
        liste_des_vins = cave.get_cards_vins(not switch_collapse_on_off, options, text_search)
        options_values = [option.get_choices(cave.actives_vins) for option in cave.options]
    #logging.debug(f"Liste_des_vins : {liste_des_vins}")
    return [liste_des_vins, options_values]

@app.callback(
    [
        Output("dialogue_add", "is_open"),
        Output('load_page', "n_clicks"),
        [Output(id, 'value') for id in cave.get_input_ids('dialogue_add_vin')], #Les champs de la boite de dialogue ADD
        Output("dialogue_details", "is_open"),
        [Output(id, 'value') for id in cave.get_input_ids('dialogue_details_vin')], #Les champs de la boite de dialogue DETAILS
    ],
    [
        Input("button_add_vin", "n_clicks"),
        Input("dialogue_add_vin_button_add", "n_clicks"),
        Input("dialogue_details_vin_button_save", "n_clicks"),
        Input({'type': 'dynamic_bt_edit', 'index': dash.ALL}, 'n_clicks'),
    ],
    [
        State("liste_des_vins", "children"),
        State("dialogue_add", "is_open"),
        State("load_page", "n_clicks"),
        {id : State(id, 'value') for id in cave.get_input_ids('dialogue_add_vin')}, #Les champs de la boite de dialogue ADD
        State("dialogue_details", "is_open"),
        {id : State(id, 'value') for id in cave.get_input_ids('dialogue_details_vin')}, #Les champs de la boite de dialogue DETAILS
        State({'type': 'dynamic_bt_edit', 'index': dash.ALL}, 'id'),
    ]
) #n_save, dynamic_bt_edit_n_clicks, liste_des_vins, is_open, load_page_n_clicks, values, dynamic_bt_edit_id
def toggle_dialogue_add(
                button_add_vin_n_clicks,
                dialogue_add_vin_button_add_n_click,
                dialogue_details_vin_button_save_n_clicks,
                dynamic_bt_edit_n_clicks,
                liste_des_vins,
                dialogue_add_is_open,
                load_page_n_clicks,
                dialogue_add_vin_values,
                dialogue_details_is_open,
                dialogue_details_vin_values,
                dynamic_bt_edit_id
                ):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    # Validation de la boite de dialogue ADD
    if  changed_id == "dialogue_add_vin_button_add.n_clicks":
        logging.debug(f"Ajout du vin. values = {dialogue_add_vin_values}")
        cave.bdd_insert('dialogue_add_vin', dialogue_add_vin_values)
        load_page_n_clicks = load_page_n_clicks or + 1 #Pour recharger la liste des vins
        dialogue_add_vin_values= [None for id in cave.get_input_ids('dialogue_add_vin')]
    # Ouverture du détails d'une card
    elif liste_des_vins and re.match('{"index":"CardVin_\d+_bt_edit","type":"dynamic_bt_edit"}.n_clicks', changed_id):
        bt_id = re.search(r"CardVin_\d+_bt_edit", changed_id).group(0)
        index = [x['index'] for x in dynamic_bt_edit_id].index(bt_id)
        if dynamic_bt_edit_n_clicks[index]: # TODO : changer ça : quand le bouton a été cliké une fois => pas remis à 0!!!
            vin = cave.get_active_vin_by_card_id(liste_des_vins[index]['props']['id'])
            dialogue_details_vin_values = cave.get_input_values(vin)
            logging.debug(f"BT {bt_id} pressed pour {vin}")
            dialogue_details_is_open = True
            load_page_n_clicks = load_page_n_clicks or + 1 #Pour recharger la liste des vins
    # Validation de la boite de dialogue details
    elif dialogue_details_vin_button_save_n_clicks:
        #TODO : appliquer modifs
        dialogue_details_vin_values = [None for id in cave.get_input_ids('dialogue_details_vin')]
        dialogue_details_is_open = False
        load_page_n_clicks = load_page_n_clicks or + 1 #Pour recharger la liste des vins
    # Ouverture / fermeture de la boite de dialogue ADD
    if button_add_vin_n_clicks or dialogue_add_vin_button_add_n_click:
        dialogue_add_is_open = not dialogue_add_is_open
        load_page_n_clicks = load_page_n_clicks or + 1 #Pour recharger la liste des vins
    #Bricolo pour si ça n'a pas été fait ailleurs, changer les dict en list
    if type(dialogue_add_vin_values)==dict:
        dialogue_add_vin_values = list(dialogue_add_vin_values.values())
    if type(dialogue_details_vin_values)==dict:
        dialogue_details_vin_values = list(dialogue_details_vin_values.values())

    return [dialogue_add_is_open, load_page_n_clicks, dialogue_add_vin_values, dialogue_details_is_open,dialogue_details_vin_values]


