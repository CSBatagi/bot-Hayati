import openai
import re

# Set up OpenAI API credentials
openai.api_key = os.getenv('OPEN_API_KEY')

# Define function to generate text using GPT-3
def generate_text(prompt, model = 'text-davinci-002', max_tokens=1024, temperature=0.5):
    response = openai.Completion.create(
        engine=model,
        prompt=prompt,
        max_tokens=max_tokens,
        temperature=temperature
    )
    text = response.choices[0].text
    return text

# Define function to clean up generated text
def clean_text(text):
    # Remove newline characters
    text = text.replace('\n', ' ')
    
    # Remove multiple spaces
    text = re.sub('\s+', ' ', text).strip()
    
    return text