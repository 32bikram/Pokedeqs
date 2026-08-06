#IDENTIFIES THE CARD USING OPENAI
# from openai import OpenAI
from google import genai
from google.genai import types

from application import config

def call_llm(image_bytes):
    prompt = '''You are an expert Pokémon card identifier.
                Analyze the uploaded Pokémon card.
                specially focus on its set name(i.e. crown zeinth, scarlet violet, paledian fates etc.)
                and the unique id of that card in the set.
                Return ONLY valid JSON. proper formating of json is must. opening and closing bracket and colons.
                Schema:
                {
                    "pokemon_name": "",
                    "card_name": "",
                    "set_name": "",
                    "card_number": ""
                }
                Rules:
                - Do not include markdown.
                - Do not include explanations.
                - Do not wrap the JSON in ```json.
                - If a field cannot be determined, return null.'''

    client = genai.Client(api_key=config.settings.llm_api)

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            prompt,
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/jpeg",
            ),
        ],
        config=types.GenerateContentConfig(
            max_output_tokens=1000,
            temperature=0,
        ),
    )

    return response.text