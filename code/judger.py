from google import genai
import os
import sys
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
grades_dir = repo_root / "dataset" / "grades"
grades_dir.mkdir(parents=True, exist_ok=True)

prompt_path = repo_root / "llm_judge_prompt.md"
prompt_text = prompt_path.read_text(encoding="utf-8")

if len(sys.argv) < 3:
    print(
        "Usage: python judger.py <input_response.json> <output_grade.json>",
        file=sys.stderr,
    )
    sys.exit(1)

response_name = sys.argv[1]
output_name = sys.argv[2]

response_path = Path(response_name)
if not response_path.is_absolute():
    if response_path.exists():
        pass
    elif (repo_root / response_path).exists() or len(response_path.parts) > 1:
        response_path = repo_root / response_path
    else:
        response_path = convos_dir / response_path.name
response_text = response_path.read_text(encoding="utf-8").strip()
output_path = Path(output_name)
if not output_path.is_absolute():
    if len(output_path.parts) > 1:
        output_path = repo_root / output_path
    else:
        output_path = grades_dir / output_path.name
output_path.parent.mkdir(parents=True, exist_ok=True)

placeholder = "[PASTE THE ENTIRE CONVERSATION IN JSON FORMAT HERE]"
if placeholder in prompt_text:
    prompt_text = prompt_text.replace(placeholder, response_text)
else:
    prompt_text = f"{prompt_text}\n\nFULL CONVERSATION - JSON FORMAT\n\n{response_text}\n"


with output_path.open("a", encoding="utf-8") as f:
        # f.write("[\n")  # Initialize the file with an empty JSON array
    

        # for i in range(3):
        response = client.models.generate_content(
                model="gemini-3-flash-preview", contents=prompt_text
        )

        f.write(response.text)
        print(response.text)
        # f.write(",\n" if i < 2 else "\n")  # Add a comma after each conversation except the last one

        # f.write("]")  # Close the JSON array

# print(response.text)

# get 2nd conversation and print it out

# with open(output_path, "r", encoding="utf-8") as f:
#         convos = json.load(f)
#         print(convos[1])  # Print the 2nd conversation (0-indexed)