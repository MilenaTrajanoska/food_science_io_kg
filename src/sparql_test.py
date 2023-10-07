from rdflib import Graph

from common.sparql_queries import recipes_with_less_than_50_g_carbohydrates as query

from config import ProjectConfig


if __name__ == '__main__':
    g = Graph()
    g.parse(ProjectConfig.target_kg_path, format=ProjectConfig.kg_format)
    qres = g.query(query)

    for res in qres:
        print(res)