from pathlib import Path

def get_project_root():
    return Path(__file__).parent.parent

KG_PATH = f"{get_project_root()}/ontology"
DATA_PATH = f"{get_project_root()}/data"

FORMAT = 'turtle'
PREFIX = 'http://example.org/recipe-ontology#'
