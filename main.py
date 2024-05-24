"""
This script demonstrates how to use the Google AI Python SDK to interact with the Gemini API.
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""
# Path: main.py

import os
import vertexai
import vertexai.preview.generative_models as generative_models
from vertexai.generative_models import GenerativeModel

GCLOUD_PROJECT_ID = os.environ["GCLOUD_PROJECT_ID"]


def print_introduction(name):
    print(f"Welcome to {name}!")
    print("This script demonstrates how to use the Google AI Python SDK to interact with the Gemini API.")
    print("Install the Google AI Python SDK")
    print("\n$ pip install google-cloud-aiplatform\n")
    print("See the getting started guide for more information:")
    print("https://ai.google.dev/gemini-api/docs/get-started/python\n")


def generate():
    vertexai.init(project=GCLOUD_PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-preview-0514")
    responses = model.generate_content(
        [text1],
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    for response in responses:
        print(response.text, end="")


text1 = """
Context : As sql specialist in Postgres 12 and up you help people optimize any SQL queries and can answer 
any questions about DDL and SQL giving advice and explaining why your code is more efficient. you work step by step 
explaining and asking questions as needed to give the more useful pragmatic answers you can even give some 
spontaneous tips and tricks on how to optimize SQL queries. 
Question : write DDL for storing a complete building information, owner and address should be normalized as needed 
in separate tables, pk index should always be named id. you can store geometry by using Postgis
"""

generation_config = {
    "max_output_tokens": 8192,
    "temperature": 1,
    "top_p": 0.95,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

if __name__ == '__main__':
    print_introduction('the SQL expert chatbot')
    generate()
