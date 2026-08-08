#IDENTIFIES THE CARD USING OPENAI
# from openai import OpenAI
from fastapi import HTTPException, status
from google import genai
from google.genai import types

from application import config

def call_llm(image_bytes):
    prompt = '''You are an expert Pokémon card identifier.
                Analyze the uploaded Pokémon card.
                specially focus on its set name(i.e. crown zeinth, scarlet violet, paledian fates etc.)
                and the unique id of that card in the set. card_name should follow like charizard vmax, charidard vstar.
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
                - If a field cannot be determined, return null.
                **Most important Note - only if the image isn't of a pokemon card return a single word -> None
                '''

    client = genai.Client(api_key=config.settings.llm_api)
    try:
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
                max_output_tokens=900,   #minimum 800 works
                temperature=0,
            ),
        )
        if(response.text=="None"):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Not a card image"
            )
        return response.text
    except:
        raise HTTPException(
            status_code = status.HTTP_402_PAYMENT_REQUIRED,
            detail = "Not enough api token"
        )