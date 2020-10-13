import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from components import graph_database

# import necessary functions from components/functions.py if needed

from app import app 

# Nav Bar
LOGO = app.get_asset_url('logo.png')  # update logo.png in assets/

# nav item links
nav_items = dbc.Container([
    # dbc.NavItem(dbc.NavLink('App 1', href='/app1')),
    # dbc.NavItem(dbc.NavLink('App 2', href='/app2'))
]
)

# navbar with logo
navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo/brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(dbc.NavbarBrand("ESSC Search", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/",  # comment out to remove main page link
            ),
            dbc.NavbarToggler(id="navbar-toggler"),
            dbc.Collapse(
                dbc.Nav(
                    [nav_items], className="ml-auto", navbar=True
                ),
                id="navbar-collapse",
                navbar=True
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-5"
)

# define layout items

# instructions
text = dcc.Markdown(
    """
    This application supports keyword-driven search of the LAC ESSC Projects
    Database. The Database provides access to knowledge from LAC ESSC projects
    captured in reports and write ups.
    
    **Use the search bar to search projects and reports by tag. Filter results 
    to find the resource you need.**
    """
)

# search bar

# options
_option_list = graph_database.get_options()
options = [
    {'label': option, 'value': option} for option in _option_list
]

search_bar = dcc.Dropdown(
    id='search_bar',
    options=options,
    placeholder="Search by tag",
    multi=True
)

# filters

SIDEBAR_STYLE = {
    # "position": "fixed",
    # "top": 0,
    # "left": 0,
    # "bottom": 0,
    # "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}


# region/country
country_filter = dbc.FormGroup(
    [
        dbc.Label('Region'),
        dcc.Dropdown(
            id='country_filter',
            multi=True
        )
    ]
)

# income group
income_filter = dbc.FormGroup(
    [
        dbc.Label('Income Group'),
        dcc.Dropdown(
            id='income_filter',
            multi=True
        )
    ]
)

# category
category_filter = dbc.FormGroup(
    [
        dbc.Label('Category'),
        dcc.Dropdown(
            id='category_filter',
            multi=True
        )
    ]
)

# sector
sector_filter = dbc.FormGroup(
    [
        dbc.Label('Sector'),
        dcc.Dropdown(
            id='sector_filter',
            multi=True
        )
    ]
)


# Filter Sidebar
filters = html.Div(
    [
        html.H2("Filter"),
        html.Hr(),
        html.P(
            "Filter search results"
        ),
        country_filter,
        income_filter,
        category_filter,
        sector_filter,
    ],
    style=SIDEBAR_STYLE,
)


# primary tags
tag_buttons = [
    dbc.Button(tag, id=tag, color='secondary', className='mr-1', size='large',
               block=True)\
     for tag in _option_list[:11]
]

# Tag Sidebar
top_tags = html.Div(
    [
        html.H2("Top Tags"),
        html.Hr(),
        html.P(
            "Select from top tags"
        ),
        tag_buttons[0],
        tag_buttons[1],
        tag_buttons[2],
        tag_buttons[3],
        tag_buttons[4],
        tag_buttons[5],
        tag_buttons[6],
        tag_buttons[7],
        tag_buttons[8],
        tag_buttons[9],
        tag_buttons[10]
    ],
    style=SIDEBAR_STYLE,
)

# results
results = dcc.Loading(
    html.Div(
        id='results'
    )
)

# define layout 
layout = html.Div([
    navbar,
    dbc.Container(
        [
            text,
            html.Br()
        ],
    ),
    dbc.Row(
        [
            dbc.Col(filters, width=2),
            dbc.Col([
                search_bar,
                html.Br(),
                results
             ], width=8),
            dbc.Col(top_tags, width=2)
        ]
    ),
    dcc.Store(id='results_store')  
])
