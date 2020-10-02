import dash
import dash_bootstrap_components as dbc
import dash_auth
import json
import os
from neo4j import GraphDatabase

external_stylesheets = [dbc.themes.YETI]  # Also try LITERA, SPACELAB

app = dash.Dash(__name__, 
                external_stylesheets=external_stylesheets, 
                show_undo_redo=False)
server = app.server
app.config.suppress_callback_exceptions = True

# UNCOMMENT FOR BASIC AUTHENTICATION
# # Keep this out of source code repository - save in a file or a database
# # Local dev
# try:
#     with open('secrets/passwords.json') as f:
#         VALID_USERNAME_PASSWORD_PAIRS = json.load(f)
# # Heroku dev
# except:
#     json_creds = os.environ.get("VALID_USERNAME_PASSWORD_PAIRS")
#     VALID_USERNAME_PASSWORD_PAIRS = json.loads(json_creds)

# auth = dash_auth.BasicAuth(
#     app,
#     VALID_USERNAME_PASSWORD_PAIRS
# )

graphenedb_url = os.environ.get("GRAPHENEDB_BOLT_URL")
graphenedb_user = os.environ.get("GRAPHENEDB_BOLT_USER")
graphenedb_pass = os.environ.get("GRAPHENEDB_BOLT_PASSWORD")

driver = GraphDatabase.driver(graphenedb_url, auth=(graphenedb_user, graphenedb_pass), encrypted=True)

session = driver.session()

session.run("MATCH (:Person {name: 'Tom Hanks'})-[:ACTED_IN]->(tomHanksMovies) RETURN movies")

def print_count(tx):
    for record in tx.run(query):
        print(record["movies"]["title"])

with driver.session() as session:
    session.read_transaction(print_count)