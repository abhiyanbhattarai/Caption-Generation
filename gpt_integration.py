import json
import openai
from openai import OpenAI


# Load your API key from the config file
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# openai.api_key = config.get('openai_api_key')


client = OpenAI(api_key=config.get('openai_api_key'))


def generate_gpt_caption(generated_caption,sentiment):

    # Generate OpenAI API request
    system_message = "You are generating a instagram caption with some words and hashtags."
    user_message = f"{sentiment} {generated_caption}"

    # Call OpenAI API
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ]
    )

    # Get the generated caption from OpenAI API response
    caption = completion.choices[0].message

    return caption.content