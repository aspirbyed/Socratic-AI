from pathlib import Path
import json
import os
import sys

import requests

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    # Fall back to environment variables if python-dotenv is not installed.
    pass

api_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/api/chat")
model = os.getenv("LOCAL_LLM_MODEL", "llama3.1:8b")

if len(sys.argv) < 2:
    print(
        "Usage: python local_llama_generator.py <output_convos.json>",
        file=sys.stderr,
    )
    sys.exit(1)

output_name = sys.argv[1]
dataset_size = sys.argv[2] if len(sys.argv) > 2 else "3"

repo_root = Path(__file__).resolve().parents[1]
convos_dir = repo_root / "dataset" / "convos"
convos_dir.mkdir(parents=True, exist_ok=True)

prompt_path = repo_root / "dataset_generation_prompt.md"
prompt_text = prompt_path.read_text(encoding="utf-8")
output_path = Path(output_name)
if not output_path.is_absolute():
    if len(output_path.parts) > 1:
        output_path = repo_root / output_path
    else:
        output_path = convos_dir / output_path.name
output_path.parent.mkdir(parents=True, exist_ok=True)


with output_path.open("w", encoding="utf-8") as f:
        f.write("[\n")

        for i in range(int(dataset_size)):
                response = requests.post(
                        api_url,
                        json={
                                "model": model,
                                "messages": [
                                        {"role": "user", "content": prompt_text}
                                ],
                                "stream": False,
                        },
                        timeout=120,
                )
                response.raise_for_status()

                content = response.json()["message"]["content"].strip()
                if content.startswith("```"):
                        content = "\n".join(content.splitlines()[1:-1]).strip()

                f.write(content)
                f.write(",\n" if i < int(dataset_size) - 1 else "\n")

                print(f"Generated conversation {i+1}/{dataset_size}")

        
        f.write("]")

with open(output_path, "r", encoding="utf-8") as f:
        convos = json.load(f)
        print(convos[1])