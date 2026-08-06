from openai import OpenAI
from .. import config

def call_llm():
    client = OpenAI(
        api_key = config.settings.llm_api,
        base_url = "https://openrouter.ai/api/v1"
    )
    response = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {"role": "user", "content": "Hello"}
        ]
    )
    print(response)
