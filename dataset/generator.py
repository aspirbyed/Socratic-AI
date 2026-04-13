from google import genai
import os
from pathlib import Path

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # Fall back to environment variables if python-dotenv is not installed.
    pass

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in environment or .env file")

client = genai.Client(api_key=api_key)

prompt_path = Path(__file__).resolve().parents[1] / "dataset_generation_prompt.md"
prompt_text = prompt_path.read_text(encoding="utf-8")

response = client.models.generate_content(
    model="gemini-3-flash-preview", contents=prompt_text
)
output_path = Path(__file__).resolve().parent / "response.json"
output_path.write_text(response.text, encoding="utf-8")
print(response.text)
