ingredients_having_at_least_15_g_protein = """
SELECT DISTINCT ?ingredient ?ingredientLabel ?amount ?nutrient ?nutrientName
WHERE {
  ?ingredient a <http://example.org/recipe-ontology#IngredientClass> ;
          rdfs:label ?ingredientLabel ;
          <http://example.org/recipe-ontology#hasNutrient> ?nutrient .

  ?nutrient <http://example.org/recipe-ontology#hasQuantity> ?amount ;
            rdfs:label ?nutrientName;
            <http://example.org/recipe-ontology#unitMeasure> ?measure .

  FILTER (?measure = "G" && xsd:decimal(?amount) >= 15.0 && CONTAINS(?nutrientName, 'Protein'))
}
"""