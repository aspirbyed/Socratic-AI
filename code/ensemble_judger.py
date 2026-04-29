from google import genai
import os
import sys
from pathlib import Path
import json
import requests

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
    "Usage: python ensemble_judger.py <input_response.json> <output_judge_grades.json>",
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

start=0

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


      #gemini always some limit problem
      with output_path.open("a", encoding="utf-8") as f:

              # response = client.models.generate_content(
              #         model="gemini-2.5-flash-lite", contents=prompt_text
              # )
              api_key = os.getenv("OR_key3")
              if not api_key:
                  raise ValueError("Missing OPENROUTER_API_KEY in environment or .env file")

              response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                  "Authorization": f"Bearer {api_key}",
                },
                data=json.dumps({
                  "model": "meta-llama/llama-3.3-70b-instruct:free", # Optional
                  "messages": [
                    {
                      "role": "user",
                      "content": prompt_text
                    }
                  ]
                })
              )

              response.raise_for_status()
              response_json = response.json()
              qwen_text = ""
              if isinstance(response_json.get("choices"), list) and response_json["choices"]:
                  qwen_text = response_json["choices"][0].get("message", {}).get("content", "")
              elif isinstance(response_json.get("message"), dict):
                  qwen_text = response_json["message"].get("content", "")
              elif isinstance(response_json.get("output_text"), str):
                  qwen_text = response_json.get("output_text", "")

              if not qwen_text:
                  raise ValueError(f"Unexpected Qwen response format: {response_json}")


              if(start==0):
                  f.write("[\n")  # Initialize the file with an empty JSON array]")
                  start=1
              else :
                  f.write(",\n")  # Add a comma before the next response if it's not the first one
              f.write(qwen_text)
              # f.write(response.text)
              # print(response.text)

      print("llama DONE")
      # print("gemini judge done")

      api_key = os.getenv("OR_key")
      if not api_key:
          raise ValueError("Missing OPENROUTER_API_KEY in environment or .env file")

      response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
          "Authorization": f"Bearer {api_key}",
        },
        data=json.dumps({
          "model": "openai/gpt-oss-20b:free", # Optional
          "messages": [
            {
              "role": "user",
              "content": prompt_text
            }
          ]
        })
      )


      print("OR DONE")
      with output_path.open("a", encoding="utf-8") as f:
              f.write(",\n")  # Add a comma after the Gemini response
              f.write(response.json()["choices"][0]["message"]["content"])
              # f.write("\n]")  # Close the JSON array

      api_key = os.getenv("OR_key2")
      if not api_key:
          raise ValueError("Missing OPENROUTER_API_KEY in environment or .env file")

      response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
          "Authorization": f"Bearer {api_key}",
        },
        data=json.dumps({
          "model": "openai/gpt-oss-120b:free", # Optional
          "messages": [
            {
              "role": "user",
              "content": prompt_text
            }
          ]
        })
      )


      print("OR DONE")
      with output_path.open("a", encoding="utf-8") as f:
              f.write(",\n")  

              # print(response.text)
              f.write(response.json()["choices"][0]["message"]["content"])

with output_path.open("a", encoding="utf-8") as f:
      f.write("\n]")  # Close the JSON array     

