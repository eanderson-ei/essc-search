"""read queries from graph database"""
from py2neo import Graph, Node, Relationship, NodeMatcher

# database info
PORT = 'bolt://localhost:7687'
PASSWORD = 'incentives'

# connect to database
graph = Graph(PORT, auth=('neo4j', PASSWORD))

# create matcher
matcher = NodeMatcher(graph)

