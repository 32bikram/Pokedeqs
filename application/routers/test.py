from openai import OpenAI
from application import config

def call_llm(base64_image):
    client = OpenAI(
        api_key = config.settings.llm_api,
        base_url = "https://openrouter.ai/api/v1"
    )
    prompt = '''You are an expert Pokémon card identifier.
                Analyze the uploaded Pokémon card.
                specially focus on its set name(i.e. crown zeinth, scarlet violet, paledian fates etc.)
                and the unique id of that card in the set.
                Return ONLY valid JSON.
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

    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages = [
            {
                "role" : "user",
                "content" : [
                    {
                        "type" : "text",
                        "text" : prompt
                    },
                    {
                        "type" : "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ]
    )
    print(response.choices[0].message.content)