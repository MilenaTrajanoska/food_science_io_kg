from rdflib import Graph

from src.common.sparql_queries import ingredients_having_at_least_15_g_protein as query

from config import (
    KG_PATH,
    FORMAT
)


if __name__ == '__main__':
    g = Graph()
    g.parse(f"{KG_PATH}/recipe_ontology_v1.0.ttl", format=FORMAT)
    qres = g.query(query)

    for res in qres:
        print(res)