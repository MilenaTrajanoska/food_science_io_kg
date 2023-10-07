from rdflib import Graph

from common.sparql_queries import recipes_with_less_than_50_g_carbohydrates as query

from config import (
    KG_PATH,
    FORMAT
)


if __name__ == '__main__':
    g = Graph()
    g.parse(f"{KG_PATH}/recipe_ontology_v2.0_small.ttl", format=FORMAT)
    qres = g.query(query)

    for res in qres:
        print(res)