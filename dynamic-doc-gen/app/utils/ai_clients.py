"""
Utility module for AI (OpenAI) client interactions.
"""
import os
import openai

# Load API key from environment variable.
openai.api_key = os.getenv("OPENAI_API_KEY", "")

# Default model (can be overridden by environment).
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

async def generate_content(system_prompt: str, user_prompt: str) -> str:
    """
    Use OpenAI's ChatCompletion API to generate content based on given prompts.
    :param system_prompt: The system level instructions for the AI.
    :param user_prompt: The user query or request for content generation.
    :return: Generated content as a string.
    """
    # Perform the API call to OpenAI (async).
    response = await openai.ChatCompletion.acreate(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    # Extract the assistant's reply content.
    content = response["choices"][0]["message"]["content"]
    # Strip any trailing whitespace/newlines for cleanliness.
    return content.strip()
