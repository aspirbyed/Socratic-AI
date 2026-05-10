import os

import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

url = "https://integrate.api.nvidia.com/v1/chat/completions"

payload = {
    "messages": [
        {
            "role": "system",
            "content": "hiiiii",
        }
    ],
    "model": "qwen/qwen3.5-397b-a17b",
    "max_tokens": 16384,
    "stream": False,
    "temperature": 0.6,
    "top_p": 0.95,
    "top_k": 20,
    "presence_penalty": 0,
}

headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": f"Bearer {os.getenv('nvidia_api_key')}",
}

response = requests.post(url, json=payload, headers=headers, timeout=300)
print(response.text)
