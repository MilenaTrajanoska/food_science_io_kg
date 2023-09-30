from rdflib import Graph, BNode, Literal
from rdflib.namespace import RDF, XSD, RDFS
import numpy as np
import tqdm

from config import (
    KG_PATH, 
    FORMAT,
    PREFIX, 
    DATA_PATH
)

from src.common.utils import (
    load_json_contents_from_file,
    load_pickle_contents_from_file
)

from src.common.namespaces import (
   RecipeNamespace
)


def calculate_quantity(qty):
  try:
    return eval(qty)
  except Exception as e:
    try:
      parts = qty.split(" ")
      return np.sum([eval(p) for p in parts])
    except Exception as e:
      raise e


if __name__ == '__main__':
  data = load_json_contents_from_file(f"{DATA_PATH}/recipe_1m/1k.json")
  mapping_dict = load_pickle_contents_from_file(f"{DATA_PATH}/food_mapping.pkl")
  g = Graph()
  g.parse(f"{KG_PATH}/recipe_ontology_v1.0.ttl", format=FORMAT)
  
  ns = RecipeNamespace(PREFIX) 
  
  food_class_nodes = []
  for s, p, o in g.triples((None, RDF.type, ns.ingredient_class_type)):
    if s not in food_class_nodes:
      food_class_nodes.append(s)
  
  fc_nodes_mapping = {}

  for fc in food_class_nodes:
    for s, p, o in g.triples((fc, RDFS.label, None)):
        fc_nodes_mapping[o] = fc
        break

  for r in tqdm.tqdm(data):
    title = r['title']
    url = r['url']
    ingredients = r['ingredients']

    b_recipe = BNode()
    g.add((b_recipe, RDF.type, ns.recipe_type))
    g.add((b_recipe, RDFS.label, Literal(title, datatype=XSD.string)))
    g.add((b_recipe, RDFS.seeAlso, Literal(url, datatype=XSD.string)))

    for i in ingredients:
        if i['name']:
            i['food_class'] = mapping_dict.get(i['name'])
        else:
            i['food_class'] = None

    for i in ingredients:
        b_ingredient = BNode()

        g.add((b_ingredient, RDF.type, ns.ingredient_type))
        g.add((b_ingredient, RDFS.label, Literal(i["name"],  datatype=XSD.string)))
        g.add((b_ingredient, ns.unit_measure_prop, Literal(i["unit"],  datatype=XSD.string)))

        if i['quantity']:
            try:
                qty = calculate_quantity(i['quantity'])
                g.add((b_ingredient, ns.has_quantity_prop, Literal(qty,  datatype=XSD.decimal)))
            except Exception as e:
                print(e, i["quantity"])

        g.add((b_recipe, ns.has_ingredient_prop, b_ingredient))

        match_fc = fc_nodes_mapping.get(Literal(i['food_class'], datatype=XSD.string))

        if match_fc:
            g.add((b_ingredient, ns.has_ingredient_class, match_fc))
    
    g.serialize(destination=f"{KG_PATH}/recipe_ontology_v2.0.ttl", format=FORMAT)