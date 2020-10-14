import dash
from dash.dependencies import Input, Output, State, ALL
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import dash_html_components as html
import pandas as pd

# import necessary functions from components/functions.py if needed
from components import graph_database

from app import app

PAGE_LIMIT = 10


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
def query_reports(search_tags):
    if search_tags:
        result = graph_database.get_report(search_tags)
        return result.to_dict('records')
    else:
        return {}

# Populate filter options
filter_dict = {
    'country_filter': 'Country',
    'income_filter': 'Income Group',
    'category_filter': 'Category',
    'sector_filter': 'Sector'
    }

# country filter
@app.callback(
    [Output('country_filter', 'options'),
     Output('country_filter', 'value')],
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
        return options, None
    else:
        return [{'label': '', 'value': ''}], None


# income filter
@app.callback(
    [Output('income_filter', 'options'),
    Output('income_filter', 'value')],
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
        return options, None
    else:
        return [{'label': '', 'value': ''}], None
    

# category filter
@app.callback(
    [Output('category_filter', 'options'),
    Output('category_filter', 'value')],
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
        return options, None
    else:
        return [{'label': '', 'value': ''}], None
    

# sector filter
@app.callback(
    [Output('sector_filter', 'options'),
     Output('sector_filter', 'value')],
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
        return options, None
    else:
        return [{'label': '', 'value': ''}], None


# Filter results
@app.callback(
    Output('filtered_results', 'children'),
    [Input('results_store', 'children'),
     Input('country_filter', 'value'),
     Input('income_filter', 'value'),
     Input('category_filter', 'value'),
     Input('sector_filter', 'value')]
)
def filter_results(results_store,
                   country_filter,
                   income_filter,
                   category_filter,
                   sector_filter):
    if not results_store:
        return {}
    
    df = pd.DataFrame(results_store)
    
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
    
    return df.to_dict('records')

# Update page store
@app.callback(
    Output('page_store', 'children'),
    [Input('back_button', 'n_clicks'),
     Input('forward_button', 'n_clicks'),
     Input('search_bar', 'value'),
     Input('country_filter', 'value'),
     Input('income_filter', 'value'),
     Input('category_filter', 'value'),
     Input('sector_filter', 'value')],
     [State('page_store', 'children')]
)
def paginate(back, forward, search_bar, f1, f2, f3, f4, page_store):
    ctx = dash.callback_context

    # initialize page_store
    if not page_store:
        page_store = {
            'start': 0,
            'end': PAGE_LIMIT
        }
    
    if ctx.triggered:
        start = int(page_store.get('start'))
        end = int(page_store.get('end'))
        trigger = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if trigger == 'search_bar':
            page_store = {
                'start': 0,
                'end': PAGE_LIMIT
            }
        elif trigger in ['country_filter', 'income_filter', 'category_filter', 'sector_filter']:
            page_store = {
                'start': 0,
                'end': PAGE_LIMIT
            }
        elif trigger == 'back_button':
            page_store['start'] = start - PAGE_LIMIT
            page_store['end'] = end - PAGE_LIMIT
            
        elif trigger == 'forward_button':
            page_store['start'] = start + PAGE_LIMIT
            page_store['end'] = end + PAGE_LIMIT
    
    return page_store


# Store tags
@app.callback(
    Output('tags_store', 'children'),
    [Input('page_store', 'children'),
     Input('filtered_results', 'children'),
     Input('country_filter', 'value'),
     Input('income_filter', 'value'),
     Input('category_filter', 'value'),
     Input('sector_filter', 'value')],
     [State('tags_store', 'children')]
)
def memoize_tags(page_store, 
                 filtered_results, 
                 country_filter, 
                 income_filter, 
                 category_filter, 
                 sector_filter,
                 tags_store):
    ctx = dash.callback_context
    trigger = ctx.triggered[0]['prop_id'].split('.')[0]
    if not filtered_results:
        return {}
    if not tags_store:
        tags_store = {}
        
    df = pd.DataFrame(filtered_results)
    
    # if country_filter:
    #     filt = df['Country'].isin(country_filter)
    #     df = df.loc[filt, :]
    
    # if income_filter:
    #     filt = df['Income Group'].isin(income_filter)
    #     df = df.loc[filt, :]
    
    # if category_filter:
    #     filt = df['Category'].isin(category_filter)
    #     df = df.loc[filt, :]
    
    # if sector_filter:
    #     filt = df['Sector'].isin(sector_filter)
    #     df = df.loc[filt, :]
        
        
    # subset for pagination
    start = int(page_store.get('start', 0))
    end = int(page_store.get('end', PAGE_LIMIT))
    
    for _, result in df.iloc[start:end, :].iterrows():
        
        # get tags and build badge list
        tags = graph_database.get_tags_from_report(result['Report_ID'])
        tags_store[result['Report_ID']] = tags
    return tags_store


@app.callback(
    Output('pagination_buttons', 'hidden'),
    [Input('results', 'children')]
)
def hide_pagination(results):
    if results == "Please search for a tag above":
        return True
    else:
        return False


@app.callback(
    Output('back_button', 'disabled'),
    [Input('page_store', 'children')]
)
def deactivate_back_button(page_store):
    if int(page_store.get('start')) == 0:
        return True
    else:
        return False


@app.callback(
    Output('forward_button', 'disabled'),
    [Input('page_store', 'children'),
     Input('filtered_results', 'children')]
)
def deactivate_forward_button(page_store, filtered_results):
    if not filtered_results:
        return False  # keep active once unhidden
    elif len(filtered_results) == 0:
        return False
    elif len(filtered_results) < int(page_store.get('end')): 
        return True
    else:
        return False


# Search Results
@app.callback(
    Output('results', 'children'),
    [Input('filtered_results', 'children'),
     Input('country_filter', 'value'),
     Input('income_filter', 'value'),
     Input('category_filter', 'value'),
     Input('sector_filter', 'value'),
     Input('page_store', 'children'),
     Input('tags_store', 'children')]
)
def update_search_results(results, 
                          country_filter, 
                          income_filter, 
                          category_filter, 
                          sector_filter,
                          page_store,
                          tags_store):
    """create search cards from tags selected"""    
    # get search results
    if not results:
        return "Please search for a tag above"
    
    print(page_store)
    
    df = pd.DataFrame(results)   
    
    # if country_filter:
    #     filt = df['Country'].isin(country_filter)
    #     df = df.loc[filt, :]
    
    # if income_filter:
    #     filt = df['Income Group'].isin(income_filter)
    #     df = df.loc[filt, :]
    
    # if category_filter:
    #     filt = df['Category'].isin(category_filter)
    #     df = df.loc[filt, :]
    
    # if sector_filter:
    #     filt = df['Sector'].isin(sector_filter)
    #     df = df.loc[filt, :]

    cards = []
    
    # subset for pagination
    start = int(page_store.get('start', 0))
    end = int(page_store.get('end', PAGE_LIMIT))
    
    for _, result in df.iloc[start:end, :].iterrows():
        
        # get tags and build badge list
        tags = tags_store.get(result['Report_ID'])
        tag_pills = []
        for tag in tags:
            pill = dbc.Badge(tag, pill=True, color='secondary', className='mr-1')
            tag_pills.append(pill)
            
        # build report card
        report_card = dbc.Card(
            dbc.CardBody(
                [
                    html.H4(result['Report_Title'], 
                            className="card-title"),
                    html.H6(
                        html.A(result['Project'].upper(),
                               href='/apps/project'),
                        className="card-subtitle"),
                    html.P(
                        result['Summary'],
                        className="card-text",
                    ),
                    html.A("Report link", 
                        href=result['Link'],
                        target="_blank"),
                    html.Br(),
                    html.Div(tag_pills)
                ]
            ), style = {"margin-top": "2rem"}
        )
        cards.append(report_card)
    
    if len(cards)>0:
        return cards
    else:
        return "No results found"


@app.callback(
    Output('scroll_top', 'run'),
    [Input('forward_button', 'n_clicks'),
     Input('back_button', 'n_clicks')]
)
def scroll_to_top(forward, back):
    if forward or back:
        js = """
        var textarea = document.getElementById('results_box');
        textarea.scrollTop = 0
        """
        return js
        
