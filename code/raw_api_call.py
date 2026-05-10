import requests
from dotenv import load_dotenv
import os


def call_llm_api(api_url: str, model_name: str, api_key: str, message: str):
    """
    Make a raw POST request to an LLM API endpoint.
    
    Args:
        api_url (str): The full API endpoint URL
        model_name (str): The model identifier
        api_key (str): The API key (Bearer token)
        message (str): The user message
    
    Returns:
        Response from the API
    """

    payload = {
        "model": model_name,
        "messages": [{"role": "user", "content": message}]
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    
    response = requests.post(api_url, json=payload, headers=headers)
    response.raise_for_status()
    
    return response.json()



load_dotenv()

api_key = os.getenv("OR_key")
api_url ="https://openrouter.ai/api/v1/chat/completions"
model_name = "openai/gpt-oss-20b:free"

response = call_llm_api(api_url, model_name, api_key, "hi")
# print(response)
print(response["choices"][0]["message"]["content"])



