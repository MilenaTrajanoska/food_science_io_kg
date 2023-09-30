from rdflib import Namespace

class RecipeNamespace:
    def __init__(self, prefix) -> None:
        self.ns = Namespace(prefix)
        self.recipe_type = self.ns.Recipe
        self.ingredient_type = self.ns.Ingredient
        self.ingredient_class_type = self.ns.IngredientClass
        self.nutrient_type = self.ns.Nutrient
        self.unit_measure_prop = self.ns.unitMeasure
        self.has_quantity_prop = self.ns.hasQuantity
        self.has_nutrient_prop = self.ns.hasNutrient
        self.has_ingredient_prop = self.ns.hasIngredient
        self.has_ingredient_class_prop = self.ns.hasIngredientClass
    
    def _get_attributes_of_type(self, attr_type):
        all_attributes = dir(self)
        type_attributes = [attr for attr in all_attributes if attr.endswith(attr_type)]
        return type_attributes
    
    def get_all_types(self):
        return self._get_attributes_of_type('type')
    
    def get_all_props(self):
        return self._get_attributes_of_type('prop')