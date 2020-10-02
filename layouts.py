import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

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
_option_list = ['Amazon', 'USAID', 'Caribbean', 'Brazillian', 'Central America',
               'Southern Caribbean', 'Latin America', 'CITES', 'TRAFFIC',
               'Google Earth', 'USFS', 'Amazonian', 'IUCN', 'Coca-Cola',
               'ICWL']
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

def create_dropdown(id, options, placeholder = '', multi=False):
    options = [
        {'label': option, 'value': option} for option in options
    ]
    dropdown = dcc.Dropdown(
        id=id,
        options=options,
        placeholder=placeholder,
        multi=multi
    )
    
    return dropdown

# region
region_list = ['Brazil', 'Caribbean', 'Central America']
region_filter = dbc.FormGroup(
    [
        dbc.Label('Region'),
        create_dropdown('region_filter', region_list)
    ]
)

# income group
income_list = ['Upper Middle Income', 'Low Income']
income_filter = dbc.FormGroup(
    [
        dbc.Label('Income Group'),
        create_dropdown('income_filter', income_list)
    ]
)

# subagency
subagency_list = ['Bureau for Latin America and Caribbean']
subagency_filter = dbc.FormGroup(
    [
        dbc.Label('Subagency'),
        create_dropdown('subagency_filter', subagency_list)
    ]
)

# category
category_list = ['NGO', 'Enterprises', 'Universities & Research Institutions']
category_filter = dbc.FormGroup(
    [
        dbc.Label('Category'),
        create_dropdown('category_filter', category_list)
    ]
)

# sector
sector_list = ['General Environmental Protection', 'Energy']
sector_filter = dbc.FormGroup(
    [
        dbc.Label('Sector'),
        create_dropdown('sector_filter', sector_list)
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
        region_filter,
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
     for tag in _option_list
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

# report card

report_card_1 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Improved Coastal Watersheds and Livelihoods project", 
                    className="card-title"),
            html.H6("Improved Coastal Watershed and Livelihoods (ICWL) Project", 
                    className="card-subtitle"),
            html.P(
                "Municipalities and local communities are supported to take on a stronger role in water, waste and natural resource management. Project objectives will be achieved through three expected results: 1.Natural ecosystems and biodiversity protected and restored through climate-smart approaches 2. Sustainability of rural livelihood systems improved through climate-smart approaches 3. Effectiveness and integration of source to sea watershed governance improved",
                className="card-text",
            ),
            html.A("Report link", 
                   href="https://oceanconference.un.org/commitments/?id=31422",
                   target="_blank"),
        ]
    ), style = {"margin-top": "2rem"}
)

report_card_2 = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Final Report", 
                    className="card-title"),
            html.H6("Improved Coastal Watershed and Livelihoods (ICWL) Project", 
                    className="card-subtitle"),
            html.P(
                "In total, 1463 people were trained within the ICWL project, including microfinance associations, governance structures, municipalities and national institutions, local NGOs, children, students, park rangers, among others. Training topics included organizational processes, participative planning, environmental, wildlife and protected areas.",
                className="card-text",
            ),
            html.A("Report link", 
                   href="https://pdf.usaid.gov/pdf_docs/PA00TRMV.pdf",
                   target="_blank"),
        ]
    ), style = {"margin-top": "1rem"}
)

# results
results = html.Div(
    id='results'
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
])
