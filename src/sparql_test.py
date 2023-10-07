from rdflib import Graph

from common.sparql_queries import recipes_with_less_than_50_g_carbohydrates as query

from config import (
    TARGET_KG,
    FORMAT
)


if __name__ == '__main__':
    g = Graph()
    g.parse(TARGET_KG, format=FORMAT)
    qres = g.query(query)

    for res in qres:
        print(res)