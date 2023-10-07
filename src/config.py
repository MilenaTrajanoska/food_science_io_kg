from pathlib import Path

def get_project_root():
    return Path(__file__).parent.parent

KG_PATH = f"{get_project_root()}/ontology"
DATA_PATH = f"{get_project_root()}/data"

FORMAT = 'turtle'
PREFIX = 'http://example.org/recipe-ontology#'
ENDPOINT = "http://localhost:5000/api/v1/sparql"
TARGET_KG = f"{KG_PATH}/recipe_ontology_v2.0_small_extended.ttl"
