from rdflib import Graph, URIRef, BNode, Literal, Namespace
from rdflib.namespace import RDF, XSD, RDFS
import pandas as pd
import pickle

from config import (
    KG_PATH, 
    FORMAT,
    PREFIX, 
    DATA_PATH
)

from src.common.utils import (
    save_pickle_contents_to_file
)

from src.common.namespaces import (
   RecipeNamespace
)


NUTRIENT_DATA_PATH = f"{DATA_PATH}/food_nutrients"


if __name__ == '__main__':
    g = Graph()
    g.parse(f"{KG_PATH}/recipe_ontology_v0.1.ttl", format=FORMAT)
    food_data = pd.read_csv(f'{NUTRIENT_DATA_PATH}/food.csv')
    food_data = food_data[food_data['data_type'] == 'foundation_food']

    nutrient_data = pd.read_csv(f'{NUTRIENT_DATA_PATH}/nutrient.csv')
    nutrient_data = nutrient_data[['id', 'name', 'unit_name']]

    food_nutrient_data = pd.read_csv(f'{NUTRIENT_DATA_PATH}/food_nutrient.csv')
    food_nutrient_data = food_nutrient_data[['id', 'fdc_id', 'nutrient_id', 'amount']]
    food_nutrient_data = food_nutrient_data.dropna()

    food_nutrient_merge = food_nutrient_data.merge(food_data, on='fdc_id', how='left')
    food_nutrient_merge = food_nutrient_merge.dropna()
    food_nutrient_merge = food_nutrient_merge.drop(columns='id')
    food_nutrient_merge = food_nutrient_merge.merge(nutrient_data, left_on='nutrient_id', right_on='id', how='left')

    food_ids = food_nutrient_merge.fdc_id.unique()
    nutrient_ids = food_nutrient_merge.id.unique()

    ns = RecipeNamespace(PREFIX)

    for i, row in food_nutrient_merge.iterrows():
        food_id = row[0]
        nutrient_id = row[1]
        amount = row[2]
        food_description = row[4]
        nutrient_name = row[8]
        unit = row[9]

        b_ingr = BNode()
        b_nutr = BNode()

        g.add((b_ingr, RDF.type, ns.ingredient_class_type))
        g.add((b_ingr, RDFS.label, Literal(food_description,  datatype=XSD.string)))

        g.add((b_nutr, RDF.type, ns.nutrient_type))
        g.add((b_nutr, RDFS.label, Literal(nutrient_name,  datatype=XSD.string)))
        g.add((b_nutr, ns.has_quantity_prop, Literal(amount,  datatype=XSD.decimal)))
        g.add((b_nutr, ns.unit_measure_prop, Literal(unit,  datatype=XSD.string)))

        g.add((b_ingr, ns.has_nutrient_prop, b_nutr))

    g.serialize(destination=f"{KG_PATH}/recipe_ontology_v1.0.ttl", format=FORMAT)
    
    food_classes = food_nutrient_merge.description.unique()
    save_pickle_contents_to_file(f'{DATA_PATH}/food_classes.pkl', food_classes)
