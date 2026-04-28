from google import genai
import os
from pathlib import Path
import json

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

repo_root = Path(__file__).resolve().parents[1]
convos_dir = repo_root / "dataset" / "convos"
convos_dir.mkdir(parents=True, exist_ok=True)

prompt_path = Path(__file__).resolve().parents[1] / "dataset_generation_prompt.md"
prompt_text = prompt_path.read_text(encoding="utf-8")
output_path = convos_dir / "gemini_convos.json"


with output_path.open("a", encoding="utf-8") as f:
        f.write("[\n")  # Initialize the file with an empty JSON array
    

        for i in range(3):
                response = client.models.generate_content(
                        model="gemini-3-flash-preview", contents=prompt_text
                )

                f.write(response.text)
                f.write(",\n" if i < 2 else "\n")  # Add a comma after each conversation except the last one

        f.write("]")  # Close the JSON array

# print(response.text)

# get 2nd conversation and print it out

with open(output_path, "r", encoding="utf-8") as f:
        convos = json.load(f)
        print(convos[1])  # Print the 2nd conversation (0-indexed)