import streamlit as st
import os
import openai
from common.chat_prompt import CHAT_PROMPT, USER_PROMPT
from common.sparql_queries import (
    ingredients_having_at_least_15_g_protein, 
    recipes_with_less_than_50_g_carbohydrates
)
from common.enumerations import EntityType
from templates.htmlTemplates import css
from dotenv import load_dotenv
from config import ProjectConfig
import requests

import logging
logging.basicConfig(level=logging.INFO)


def generate_sparql(user_question):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
        {
            "role": "system",
            "content": CHAT_PROMPT.format(
                scheme_ontology=st.session_state.ontology,
                query1=ingredients_having_at_least_15_g_protein,
                query2=recipes_with_less_than_50_g_carbohydrates
            )
        },
        {
            "role": "user", 
            "content": USER_PROMPT.format(user_question=user_question)
        }
        ]
    )

    return completion.choices[0]['message']['content']


def get_response_type(response):
    if 'recipeName' in response[0].keys():
        return EntityType.RECIPE
    elif 'ingredientName' in response[0].keys():
        return EntityType.INGREDIENT
    else:
        return EntityType.UNKNOWN


def display_response_by_type(element, response_type):
    if response_type == EntityType.RECIPE:
        st.header(element.get("recipeName", ""))
        st.write(element.get("description", ""))
        st.write(element.get("link", ""))
    elif response_type == EntityType.INGREDIENT:
        st.header(element.get("ingredientName", ""))
        st.write(f"{element.get('nutrientName', '')}: {element.get('nutrientQuantity', '0')} grams")


def handle_result(response):
    if type(response) != list or len(response) == 0:
        st.write("No recipes were identified for your question")
    else:
        response_type = get_response_type(response)
        for recipe in response:
            display_response_by_type(recipe, response_type)


def set_session():
    if "ontology" not in st.session_state:
        ttl_file = open(ProjectConfig.basic_ontology_path,'r')
        st.session_state.ontology = ttl_file.read()


def main():
    st.set_page_config(page_title="RecipeKG Bot",
                       page_icon=":stew:")
    st.write(css, unsafe_allow_html=True)

    set_session()

    st.header("RecipeKG Bot :stew:")
    with st.form("formid"):
        user_question = st.text_input("Ask for a specific recipe or ingredient")
        submitted = st.form_submit_button("Send")

        if submitted:
            query = generate_sparql(user_question)
            logging.info(query)
           
            response = requests.get(ProjectConfig.sparql_endpoint, params={'query': query})
            logging.info(response.status_code)
            logging.info(response.json())

            results = response.json().get('results', 'No data could be found')
            handle_result(results)


if __name__ == '__main__':
    if os.getenv("ENVIRON") != 'prod':
        load_dotenv("../.env.dev")
    main()
