import json
import pickle
import openai


def load_json_contents_from_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


def load_pickle_contents_from_file(file_path):
    with open(file_path, 'rb') as f:
        return pickle.load(f)
    
def save_pickle_contents_to_file(file_path, content):
    with open(file_path, 'wb') as f:
        pickle.dump(content, f)
        