from dash import html, dcc
import dash_bootstrap_components as dbc
from components.cave import Cave
from components.cave_bdd import Cave_Bdd


cave = Cave(Cave_Bdd('cave.db'), 'vins')


search_bar = dbc.Row(
    dbc.Col(dbc.Input(type="search", id = "text_search", placeholder="Search")),
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

button_add = dbc.Button(
    "Ajouter un vin", color = "primary", class_name="me-2", n_clicks=0,
    id = "button_add_vin"
)

switch_collapse_on_off = dbc.Switch(
    label = "détails visibles",
    value = False,
    id = "switch_collapse_on_off",
    class_name="me-2 text-light",
)


nav_bar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="./static/images/cave.ico", height="30px")),
                    ],
                    align = "center",
                    className="g-0"
                ),
                href = "",
                style={"textDecoration": "none"}
            ),
            dbc.Col(html.H2("Ma cave"),className = "text-ligh"),
            switch_collapse_on_off,
            search_bar,
            button_add
        ]
    ),
    color = "dark",
    dark = True
)

dialoque_add_vin = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Ajout d'un vin")),
        dbc.ModalBody(cave.get_input_groups("dialogue_add_vin")),
        dbc.ModalFooter(
            dbc.Button("Add", id="dialogue_add_vin_button_add", className="ms-auto", n_clicks=0)
        ),
    ],
    id = "dialogue_add",
    is_open = False,
)


dialoque_details_vin = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Détail du vin")),
        dbc.ModalBody(cave.get_input_groups("dialogue_details_vin")),
        dbc.ModalFooter(
            dbc.Button("Sauve", id="dialogue_details_vin_button_save", className="ms-auto", n_clicks=0)
        ),
    ],
    id = "dialogue_details",
    is_open = False,
)




criteres = html.Div(id="criteres", children=cave.get_selecteurs())

liste_des_vins = dbc.Row(id="liste_des_vins")

load_page = html.Div(
    id = "load_page",
)

body = dbc.Container([
    dbc.Row(nav_bar),
    dbc.Row([
        dbc.Col(criteres, width = 3),
        dbc.Col(liste_des_vins)
        ]),
    load_page,
    dialoque_add_vin,
    dialoque_details_vin,
])



layout_index =html.Div(body)
