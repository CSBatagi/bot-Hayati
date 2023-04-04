import openai
import re
import os
from dotenv import load_dotenv


class Gpt:
    def __init__(self) -> None:
        # Set up OpenAI API credentials
        load_dotenv()
        openai.api_key = os.getenv('OPEN_API_KEY')

    # Define function to generate text using GPT-3
    def generate_text(self, prompt, model='text-davinci-003', max_tokens=1024, temperature=0.5):
        response = openai.Completion.create(
            engine=model,
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        text = response.choices[0].text
        return text

    # Define function to clean up generated text
    def clean_text(self, text):
        # Remove newline characters
        text = text.replace('\n', ' ')

        # Remove multiple spaces
        text = re.sub('\s+', ' ', text).strip()

        return text
