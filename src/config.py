from pathlib import Path
from dataclasses import dataclass
import os


def get_project_root():
    return Path(__file__).parent


@dataclass
class ProjectConfig:
    ontology_dir = f"./ontology"
    data_path = f"./data"
    basic_ontology_path = f"{ontology_dir}/recipe_ontology_v0.1.ttl"
    kg_format = 'turtle'
    kg_prefix = 'http://example.org/recipe-ontology#'
    sparql_endpoint = "http://localhost:5000/api/v1/sparql" if os.getenv("ENVIRON") != 'prod' else os.getenv("SPARQL_ENDPOINT")
    target_kg_path = f"{ontology_dir}/recipe_ontology_v2.0_small_extended.ttl"
