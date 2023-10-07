ingredients_having_at_least_15_g_protein = """
SELECT DISTINCT ?ingredient ?ingredientName ?nutrientQuantity ?nutrient ?nutrientName
WHERE {
  ?ingredient a <http://example.org/recipe-ontology#IngredientClass> ;
          rdfs:label ?ingredientName ;
          <http://example.org/recipe-ontology#hasNutrient> ?nutrient .

  ?nutrient <http://example.org/recipe-ontology#hasQuantity> ?nutrientQuantity ;
            rdfs:label ?nutrientName;
            <http://example.org/recipe-ontology#unitMeasure> ?measure .

  FILTER (?measure = "G" && xsd:decimal(?nutrientQuantity) >= 15.0 && CONTAINS(?nutrientName, 'Protein'))
}
"""

recipes_with_less_than_50_g_carbohydrates = """
SELECT DISTINCT ?recipeName ?description ?link (SUM(?totalQuantity) as ?nutrientValueTotal)
WHERE {
  ?recipe a <http://example.org/recipe-ontology#Recipe> ;
          rdfs:label ?recipeName ;
          rdfs:seeAlso ?link ;
          rdfs:comment ?description ;
          <http://example.org/recipe-ontology#hasIngredient> ?ingredient.

  ?ingredient <http://example.org/recipe-ontology#hasQuantity> ?quantity ;
          <http://example.org/recipe-ontology#unitMeasure> ?unit ;
          <http://example.org/recipe-ontology#hasIngredientClass> ?ingredientClass.

  ?ingredientClass <http://example.org/recipe-ontology#hasNutrient> ?nutrient .

  ?nutrient <http://example.org/recipe-ontology#hasQuantity> ?nutrientQuantity ;
            rdfs:label ?nutrientName;
            <http://example.org/recipe-ontology#unitMeasure> ?measure .
  
   BIND(?quantity * COALESCE(?conversionFactor, 1) * ?nutrientQuantity AS ?totalQuantity)
    
   FILTER (?measure = "G" && CONTAINS(?nutrientName, 'Carbohydrate'))
    
    # Optional: Perform unit conversion using the conversion table
    OPTIONAL {
        ?conversion <http://example.org/recipe-ontology#unitFrom> ?unit ;
                    <http://example.org/recipe-ontology#unitTo> "G"^^xsd:string ;
                    <http://example.org/recipe-ontology#conversionFactor> ?conversionFactor .
    }
}

GROUP BY ?recipeName ?description ?link
HAVING (SUM(?totalQuantity) < 50.0)
"""
  