from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

# import necessary functions from components/functions.py if needed
from layouts import report_card_1, report_card_2

from app import app


# Nav bar 
@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# Top Tags
@app.callback(
    Output('search_bar', 'value'),
    [Input('Amazon', 'n_clicks')],
    [State('search_bar', 'value')]
)
def add_tag_to_search(n1, current_values):
    if n1:
        return ['Amazon']

# Search Results
@app.callback(
    Output('results', 'children'),
    [Input('search_bar', 'value')]
)
def update_search_results(tags):
    if tags == ['ICWL']:
        return [report_card_1, report_card_2]
    else:
        return "Please search for a tag above"