"""read queries from graph database"""
from py2neo import Graph, Node, Relationship, NodeMatcher
import pandas as pd
import numpy as np

# database info
PORT = 'bolt://localhost:7687'
PASSWORD = 'incentives'

# connect to database
graph = Graph(PORT, auth=('neo4j', PASSWORD))

# create matcher
matcher = NodeMatcher(graph)

def get_options():
    """return list of tags ordered by number of relationships"""
    tags = []
    result = graph.run(
        """
        MATCH(n:Tag)-[r]-() 
        RETURN n.name, count(r) as result 
        order by result desc
        """
        )
    for record in result:
        tags.append(record['n.name'])
        
    return tags
    
    
def get_report(tags):
    """returns df of reports based on tags"""
    reports = []
    for tag in tags:
        result = graph.run(
            f"""
            MATCH(t:Tag)-[]-(r:Report)-[]-(p:Project)
            WHERE t.name = "{tag}"
            OPTIONAL MATCH (p)-[:IN]-(s)
            WHERE s:Sector OR s:Country OR s:`Income Group` OR s:Category
            RETURN r.name, r.Report_Title, r.summary, r.Link,
            p['Project Name'], labels(s), s.name
            """
            ).to_data_frame()
        result.columns = ['Report_ID', 'Report_Title', 'Summary',
                          'Link', 'Project', 'Label', 'Value']
        reports.append(result)
    reports = pd.concat(reports)
    reports['Label'] = reports['Label'].str[0]  # get labels out of list
    reports = reports.pivot(index=['Report_ID', 'Report_Title', 'Summary',
                        'Link', 'Project'], columns='Label', values='Value')
    reports = reports.reset_index()
    
    return reports
