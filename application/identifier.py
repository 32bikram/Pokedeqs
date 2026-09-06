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
                **Most important Note - If the image isn't of a pokemon card return the string -> Not a card
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
                max_output_tokens=1200,   #minimum 800 works
                temperature=0,
            ),
        )
        if(response.text=="Not a card"):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = "Not a card image"
            )
        return response.text
    except HTTPException:
        raise
    except Exception as e:
        print("Gemini error:", e)
        raise HTTPException(
            status_code = status.HTTP_402_PAYMENT_REQUIRED,
            detail = "My API limit ran out, please try after 12 P.M."
        )