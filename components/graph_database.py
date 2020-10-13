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


# def get_report(names):
#     """returns list of report nodes"""
#     reports = []
#     for name in names:
#         result = graph.run(
#             f"""
#             MATCH(n:Tag)-[r]-(m:Report)
#             WHERE n.name = "{name}"
#             RETURN m.name, m.Report_Title, m.summary, m.Link  
#             """
#             ).data()
#         for each in result: 
#             # note that each is a list of dictionaries, one per node, 
#             # with keys of the RETURN statement of the cypher query 
#             # {m.name: "", m.Report_Title:"", ...}
#             # results may also be read to a pandas dataframe if easier
#             # to process (maybe if using 'AND' search style?)
#             reports.append(each)
#         return reports
    
    
def get_report(tags):
    """returns list of report nodes"""
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
        # result = graph.run(
        #     f"""
        #     MATCH(m:Report)-[r]-(n:Project)-[]-(p)
        #     WHERE m.name = "{name}"
        #     AND p:Country OR p:`Income Group` OR p:Category OR p:Sector
        #     RETURN m, n, p
        #     """
        #     ).to_data_frame()
        
        # f"""
        #     MATCH(m:Report)-[r]-(n:Project)-[]-(p)
        #     WHERE m.name = "{name}"
        #     AND (p:Sector OR p:Country OR p:`Income Group` OR p:Category) 
        #     RETURN m.name, m.Report_Title, m.summary, m.Link,
        #     n['Project Name'], labels(p), p['name']
        #     """
        # result.to_csv(f'data/outputs/{name}.csv')
        
        # for each in result: 
        #     print(each, '\n\n')
            # note that each is a list of dictionaries, one per node, 
            # with keys of the RETURN statement of the cypher query 
            # {m.name: "", m.Report_Title:"", ...}
            # results may also be read to a pandas dataframe if easier
            # to process (maybe if using 'AND' search style?)
            # reports.append(each)
        result.columns = ['Report_ID', 'Report_Title', 'Summary',
                          'Link', 'Project', 'Label', 'Value']
        # result['Label'] = result['Label'].str[0]  # get labels out of list
        # # result = result.set_index(['Report_ID', 'Report_Title', 'Summary',
        # #                   'Link', 'Project'], append=True)
        # # result.to_csv(f'data/outputs/reports.csv')
        # result = result.pivot(index=['Report_ID', 'Report_Title', 'Summary',
        #                   'Link', 'Project'], columns='Label', values='Value')
        reports.append(result)
    reports = pd.concat(reports)
    reports['Label'] = reports['Label'].str[0]  # get labels out of list
    # reports = reports.set_index(['Report_ID', 'Report_Title', 'Summary',
    #                   'Link', 'Project'], append=True)
    # reports.to_csv(f'data/outputs/reports.csv')
    reports = reports.pivot(index=['Report_ID', 'Report_Title', 'Summary',
                        'Link', 'Project'], columns='Label', values='Value')
    reports = reports.reset_index()
    
    return reports


def get_project_from_report(report):
    result = graph.run(
        f"""
        MATCH(m:Report)-[r]-(n:Project)
        WHERE m.name = "{report}"
        RETURN n['Project Name']
        """
    ).evaluate()
    return result


def filter_results(filter_name, filter_value, report_data):
    result = graph.run(
        f"""
        MATCH()
        WHERE
        RETURN
        """
    ).data()
    return None


def get_project(name):
    """returns project"""
    project = matcher.match('Project', name=name).first()
    return project
