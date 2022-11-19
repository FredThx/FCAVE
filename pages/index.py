from dash import html, dcc
import dash_bootstrap_components as dbc

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
    id = "button_add"
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

dialoque_add = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Ajout d'un vin")),
        dbc.ModalBody([
            dbc.InputGroup(
                    [dbc.InputGroupText("Nom"), dbc.Input(id = "dialogue_add_name", placeholder="Nom du vin")],
                    className="mb-3",
                ),
            dbc.InputGroup(
                    [
                        dbc.InputGroupText("Couleur"),
                        dbc.Select(
                            options=[
                                {"label": "Rouge", "value": "blanc"},
                                {"label": "Blanc", "value": "rouge"},
                                {"label": "Rosé", "value": "rosé"},
                            ],
                            id = "dialogue_add_color",
                        ),
                    ]
                ),       
        ]),
        dbc.ModalFooter(
            dbc.Button(
                "Add", id="dialogue_add_button_add", className="ms-auto", n_clicks=0
            )
        ),
    ],
    id = "dialogue_add",
    is_open = False,
)

criteres = html.Div(id="criteres")

liste_des_vins = dbc.Row(id="liste_des_vins")

load_page = dcc.Interval(
    id = "load_page",
    n_intervals=0,
    max_intervals=0,
    interval=1
)

body = dbc.Container([
    dbc.Row(nav_bar),
    dbc.Row([
        dbc.Col(criteres),
        dbc.Col(liste_des_vins)
        ]),
    load_page,
    dialoque_add,
])



layout_index =html.Div(body)
