import dash
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

# import necessary functions from components/functions.py if needed
from components import graph_database

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
    [Input(option, 'n_clicks') for option in graph_database.get_options()[:11]]
)
def add_tag_to_search(*button_clicks):
    ctx = dash.callback_context
    
    if ctx.triggered:
        option = ctx.triggered[0]['prop_id'].split('.')[0]
        return [option]

# Store results
@app.callback(
    Output('results_store', 'children'),
    [Input('search_bar', 'value')]
)
def query_reports(tags):
    if tags:
        result = graph_database.get_report(tags)
        return result.to_dict('records')
    else:
        return {}


# # def generate_filter_callback(filter_id, results):
# def generate_filter_callbacks():
#     def filter_reports(filter_id, results):
#         if not results:
#             raise PreventUpdate
#         else:
#             filter_dict = {
#                 'country_filter': 'Country',
#                 'income_filter': 'Income Group',
#                 'category_filter': 'Category',
#                 'sector_filter': 'Sector' 
#             }
            
#             df = pd.DataFrame(results)
#             options = df[filter_dict.get(filter_id)].unique()
#             options = [
#                 {'label': option, 'value': option} for option in options
#             ]
#             return options
           
# # Update filters
# filters = ['country_filter', 'income_filter', 'category_filter', 'sector_filter']
# for filter_id in filters:
#     app.callback(
#         Output(filter_id, 'options'),
#         [Input(filter_id, 'id'),
#          Input('results_store', 'children')]
#     )(generate_filter_callbacks())

filter_dict = {
    'country_filter': 'Country',
    'income_filter': 'Income Group',
    'category_filter': 'Category',
    'sector_filter': 'Sector'
    }

@app.callback(
    Output('country_filter', 'options'),
    [Input('results_store', 'children')]
)
def update_country_filter(results):
    if results:
        filter_id = 'country_filter'
        df = pd.DataFrame(results)
        options = df[filter_dict.get(filter_id)].dropna().unique()
        options = [
            {'label': option, 'value': option} for option in options
        ]
        return options
    else:
        return [{'label': '', 'value': ''}]


@app.callback(
    Output('income_filter', 'options'),
    [Input('results_store', 'children')]
)
def update_income_filter(results):
    if results:
        filter_id = 'income_filter'
        df = pd.DataFrame(results)
        options = df[filter_dict.get(filter_id)].dropna().unique()
        options = [
            {'label': option, 'value': option} for option in options
        ]
        return options
    else:
        return [{'label': '', 'value': ''}]
    
    
@app.callback(
    Output('category_filter', 'options'),
    [Input('results_store', 'children')]
)
def update_category_filter(results):
    if results:
        filter_id = 'category_filter'
        df = pd.DataFrame(results)
        options = df[filter_dict.get(filter_id)].dropna().unique()
        options = [
            {'label': option, 'value': option} for option in options
        ]
        return options
    else:
        return [{'label': '', 'value': ''}]
    

@app.callback(
    Output('sector_filter', 'options'),
    [Input('results_store', 'children')]
)
def update_sector_filter(results):
    if results:
        filter_id = 'sector_filter'
        df = pd.DataFrame(results)
        options = df[filter_dict.get(filter_id)].dropna().unique()
        options = [
            {'label': option, 'value': option} for option in options
        ]
        return options
    else:
        return [{'label': '', 'value': ''}]
    
    
    
# @app.callback(
#     Output({'type': 'filter', 'index': ALL}, 'options'),
#     Input('results_store', 'children')]
# )
# def update_filter_options(results):
#     filter_dict = {
#             'country_filter': 'Country',
#             'income_filter': 'Income Group',
#             'category_filter': 'Category',
#             'sector_filter': 'Sector' 
#         }
#     df = pd.DataFrame(results)
#     options = df[filter_dict.get(filter_id)].unique()

# Search Results
@app.callback(
    Output('results', 'children'),
    [Input('results_store', 'children'),
     Input('country_filter', 'value'),
     Input('income_filter', 'value'),
     Input('category_filter', 'value'),
     Input('sector_filter', 'value')]
)
def update_search_results(results, 
                          country_filter, 
                          income_filter, 
                          category_filter, 
                          sector_filter):
    """create search cards from tags selected"""
    # get search results
    if not results:
        return "Please search for a tag above"
    
    df = pd.DataFrame(results)   
    
    if country_filter:
        filt = df['Country'].isin(country_filter)
        df = df.loc[filt, :]
    
    if income_filter:
        filt = df['Income Group'].isin(income_filter)
        df = df.loc[filt, :]
    
    if category_filter:
        filt = df['Category'].isin(category_filter)
        df = df.loc[filt, :]
    
    if sector_filter:
        filt = df['Sector'].isin(sector_filter)
        df = df.loc[filt, :]

    cards = []
    for _, result in df.iterrows():
        # build report card
        report_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(result['Report_Title'], 
                            className="card-title"),
                    html.H6(result['Project'].upper(), 
                            className="card-subtitle"),
                    html.P(
                        result['Summary'],
                        className="card-text",
                    ),
                    html.A("Report link", 
                        href=result['Link'],
                        target="_blank"),
                ]
            ), style = {"margin-top": "2rem"}
        )
        cards.append(report_card)
        # # get project
        # project = graph_database.get_project_from_report(result['m.name'])
        # # build report card
        # report_card = dbc.Card(
        #     dbc.CardBody(
        #         [
        #             html.H4(result['m.Report_Title'], 
        #                     className="card-title"),
        #             html.H6(project.upper(), 
        #                     className="card-subtitle"),
        #             html.P(
        #                 result['m.summary'],
        #                 className="card-text",
        #             ),
        #             html.A("Report link", 
        #                 href=result['m.Link'],
        #                 target="_blank"),
        #         ]
        #     ), style = {"margin-top": "2rem"}
        # )
        # cards.append(report_card)
    
    if len(cards)>0:
        return cards
    else:
        return "No results found"
