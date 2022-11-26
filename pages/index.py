from dash import html, dcc
import dash_bootstrap_components as dbc
from components.cave import Cave
from components.cave_bdd import Cave_Bdd

cave = Cave(Cave_Bdd('cave.db'), 'vins')

search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Search")),
        dbc.Col(
            dbc.Button(
                "Search", color="secondary", className="ms-2", n_clicks=0,
                id = "button_search"
            ),
            width="auto",
        ),
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

button_add = dbc.Button(
    "Ajouter un vin", color = "primary", class_name="me-2", n_clicks=0,
    id = "button_add_vin"
)

nav_bar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="./static/images/cave.ico", height="30px")),
                        dbc.Col(dbc.Navbar("Cave", className = "ms-2"))
                    ],
                    align = "center",
                    className="g-0"
                ),
                href = "",
                style={"textDecoration": "none"}
            ),
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
])



layout_index =html.Div(body)
