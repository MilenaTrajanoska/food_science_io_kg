import openai
import json
import time
import tqdm
from dotenv import load_dotenv

from config import ProjectConfig

from common.utils import (
    load_json_contents_from_file,
    load_pickle_contents_from_file,
    save_pickle_contents_to_file
)

from common.mapping_prompts import (
    SYSTEM_PROMPT,
    USER_PROMPT
)


def generate_food_class_mapping(ingredients, food_classes):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
           "content": SYSTEM_PROMPT
      },
      {
          "role": "user", 
          "content": USER_PROMPT.format(food_classses=food_classes, ingredients=ingredients)
       }
    ]
  )

  return json.loads(completion.choices[0]['message']['content'])


if __name__ == '__main__':
    load_dotenv()
    data = load_json_contents_from_file(f"{ProjectConfig.data_path}/recipe_1m/1k.json")
    food_classes = load_pickle_contents_from_file(f"{ProjectConfig.data_path}/food_classes.pkl")

    ing_names = set()
    for d in data:
        for i in d['ingredients']:
            ing_names.add(i['name'])

    ing_names = list(ing_names)
    mapping_set = {}

    for i in tqdm.tqdm(range(0, len(ing_names), 10)):
        ing_to_map = ing_names[i:i+10]
        try:
            ingredient_mapping = generate_food_class_mapping(ing_to_map, food_classes)
            mapping_set.update(ingredient_mapping)
            save_pickle_contents_to_file(f"{ProjectConfig.data_path}/food_mapping.pkl", mapping_set)
        except Exception as e:
            print(e)

        time.sleep(20)  # aviod rate limit
