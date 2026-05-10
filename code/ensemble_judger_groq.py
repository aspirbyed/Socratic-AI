from groq import Groq
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

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError("Missing GROQ_API_KEY in environment or .env file")

client = Groq(api_key=api_key)

repo_root = Path(__file__).resolve().parents[1]
convos_dir = repo_root / "dataset" / "convos"
grades_dir = repo_root / "dataset" / "grades"
grades_dir.mkdir(parents=True, exist_ok=True)

prompt_path = repo_root / "llm_judge_prompt.md"
prompt_text = prompt_path.read_text(encoding="utf-8")

if len(sys.argv) < 3:
    print(
        "Usage: python ensemble_judger_groq.py <input_response.json> <output_judge_grades.json>",
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

response_data = json.loads(response_path.read_text(encoding="utf-8").strip())
# Ensure response_data is an array
if isinstance(response_data, dict):
    response_data = [response_data]


def run_model(model_name: str, user_prompt: str) -> str:
    completion = client.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
    )

    content = completion.choices[0].message.content if completion.choices else ""
    if not content:
        raise ValueError(f"Unexpected Groq response format for model {model_name}")
    return content


start = 0

for convo in response_data:
    response_text = json.dumps(convo)

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
        model_text = run_model("llama-3.3-70b-versatile", prompt_text)

        if start == 0:
            f.write("[\n")
            start = 1
        else:
            f.write(",\n")
        f.write(model_text)

    print("llama DONE")

    with output_path.open("a", encoding="utf-8") as f:
        f.write(",\n")
        f.write(run_model("qwen/qwen3-32b", prompt_text))

    print("gpt-oss-20b DONE")

    with output_path.open("a", encoding="utf-8") as f:
        f.write(",\n")
        f.write(run_model("openai/gpt-oss-120b", prompt_text))

    print("gpt-oss-120b DONE")

with output_path.open("a", encoding="utf-8") as f:
    f.write("\n]")
