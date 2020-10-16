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
    reports.to_csv('data/reports.csv')
    reports = reports.drop_duplicates()
    reports = reports.pivot(index=['Report_ID', 'Report_Title', 'Summary',
                                 'Link', 'Project'],
                            columns='Label', values='Value')
    reports = reports.reset_index()
    
    return reports


def get_tags_from_report(report):
    """returns list of tags associated with a report"""
    result = graph.run(
        f"""
        MATCH(r:Report)-[]-(t:Tag)
        WHERE r.name = "{report}"
        RETURN t.name
        """
    ).data()
    result = [list(d.values()) for d in result]
    return result


def get_related_projects(project):
    """return list of related projects"""
    tags = []
    result = graph.run(
        f"""
        MATCH (p:Project {{`Project Name`: "{project}"}})-[s:SHARES_TAGS]->(p2:Project) 
        RETURN p2 
        ORDER BY s.count DESC 
        LIMIT 7
        """
        ).data()
    for record in result:
        for _, each in record.items():
            tags.append(each["Project Name"])
        
    return tags


def get_project_property(project, property):
    """returns property of a project"""
    result = graph.run(
        f"""
        MATCH (p:Project {{`Project Name`: "{project}"}})
        RETURN p["{property}"]
        """
    ).data()
    result=str([list(d.values()) for d in result][0][0])
    return result