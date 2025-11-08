from openai import OpenAI
import os

# Prefer environment variables for API configuration. If OPENAI_API_KEY is set,
# the OpenAI client will pick it up automatically.
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable not set")
client = OpenAI(api_key=api_key)

def call_openai(prompt='Write a Python function that returns the square of a number'):
    # Call the OpenAI API with the prompt
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": prompt,
            }
        ],
        model="gpt-4o",
    )
    return chat_completion


# Summarize the diagnosis as you would to a 5 year old.
# Stats Finder 
