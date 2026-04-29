from pathlib import Path
import json
import os
import sys
import random
import requests

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Setup paths
repo_root = Path(__file__).resolve().parents[1]
convos_dir = repo_root / "dataset" / "convos"
convos_dir.mkdir(parents=True, exist_ok=True)

# Load prompts from files
student_prompt_path = repo_root / "student_prompt.txt"
tutor_prompt_path = repo_root / "tutor_prompt.txt"

student_prompt_text = student_prompt_path.read_text(encoding="utf-8")
tutor_prompt_text = tutor_prompt_path.read_text(encoding="utf-8")

intensity_levels = ["high", "medium", "low"]
topics = [
    "Number series",
    "Ratio and proportion",
    "Percentages",
    "Time and work",
    "Speed, time, distance",
    "Logical puzzles",
    "Probability",
    "Coding-decoding",
    "Direction sense",
    "Blood relations",
]

selected_intelligence = random.choice(intensity_levels)
selected_cooperativeness = random.choice(intensity_levels)
selected_persistence = random.choice(intensity_levels)
selected_prior_knowledge = random.choice(intensity_levels)
selected_distraction_tendency = random.choice(intensity_levels)
selected_topic = random.choice(topics)

student_prompt_text = student_prompt_text.replace("insert_intelligence", selected_intelligence)
student_prompt_text = student_prompt_text.replace("insert_cooperativeness", selected_cooperativeness)
student_prompt_text = student_prompt_text.replace("insert_persistence", selected_persistence)
student_prompt_text = student_prompt_text.replace("insert_prior_knowledge", selected_prior_knowledge)
student_prompt_text = student_prompt_text.replace("insert_distraction_tendency", selected_distraction_tendency)
student_prompt_text = student_prompt_text.replace("insert_topic", selected_topic)

# Initialize variables
conversation_json = []
iter_count = 0
max_iterations = 20
completed_iterations = 0

# API configurations
gpt_oss_api_key = os.getenv("OR_key")
if not gpt_oss_api_key:
    raise ValueError("Missing OR_key (OpenRouter API Key) in environment or .env file")

local_llm_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/api/chat")
local_llm_model = os.getenv("LOCAL_LLM_MODEL", "llama3.1:8b")

# Main conversation loop
while iter_count < max_iterations:
    print(f"Iteration {iter_count + 1}/{max_iterations}")
    
    # Convert conversation JSON to plain text
    conversation_text = json.dumps(conversation_json, indent=2)
    
    # Prepare student prompt with conversation history
    student_prompt_with_conv = student_prompt_text.replace(
        "[PASTE THE ENTIRE CONVERSATION HERE]",
        conversation_text
    )
    
    # Call GPT-OSS 120B model via OpenRouter
    print("Calling GPT-OSS 120B model...")
    gpt_response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {gpt_oss_api_key}",
        },
        json={
            "model": "openai/gpt-oss-120b:free",
            "messages": [
                {"role": "user", "content": student_prompt_with_conv}
            ],
        },
        timeout=120,
    )
    gpt_response.raise_for_status()
    
    # Extract student response
    student_reply = gpt_response.json()["choices"][0]["message"]["content"].strip()
    
    # Add student response to conversation
    student_turn = {
        "turn": iter_count * 2 + 1,
        "speaker": "student",
        "text": student_reply
    }
    conversation_json.append(student_turn)
    print(f"Student response added (Turn {student_turn['turn']})")
    
    # Convert updated conversation JSON to plain text
    conversation_text = json.dumps(conversation_json, indent=2)
    
    # Prepare tutor prompt with updated conversation history
    tutor_prompt_with_conv = tutor_prompt_text.replace(
        "[PASTE THE ENTIRE CONVERSATION HERE]",
        conversation_text
    )
    
    # Call local Llama model
    print("Calling Llama3.1:8b model...")
    llama_response = requests.post(
        local_llm_url,
        json={
            "model": local_llm_model,
            "messages": [
                {"role": "user", "content": tutor_prompt_with_conv}
            ],
            "stream": False,
        },
        timeout=120,
    )
    llama_response.raise_for_status()
    
    # Extract and parse tutor response
    tutor_response_text = llama_response.json()["message"]["content"].strip()
    
    # Remove markdown code fences if present
    if tutor_response_text.startswith("```"):
        tutor_response_text = "\n".join(tutor_response_text.splitlines()[1:-1]).strip()
    
    # Parse JSON response from tutor
    tutor_response_json = json.loads(tutor_response_text)
    
    # Add tutor response to conversation
    tutor_turn = {
        "turn": iter_count * 2 + 2,
        "speaker": "tutor",
        "reasoning": tutor_response_json.get("reasoning", ""),
        "text": tutor_response_json.get("reply", "")
    }
    conversation_json.append(tutor_turn)
    print(f"Tutor response added (Turn {tutor_turn['turn']})")
    
    # Check if conversation should end
    should_end = tutor_response_json.get("end", 0)
    completed_iterations += 1
    if should_end == 1:
        print("Conversation ended by tutor (end=1)")
        break
    
    # Increment iterator
    iter_count += 1

# Write final conversation in llama-style format to convos/eval.json
output_path = convos_dir / "eval.json"
final_payload = [
    {
        "config": {
            "generator": "conversation_generator.py",
            "max_iterations": max_iterations
        },
        "topic": selected_topic,
        "problem": "",
        "conversation": conversation_json
    }
]

with output_path.open("w", encoding="utf-8") as f:
    json.dump(final_payload, f, indent=2)

print(f"\nConversation saved to {output_path}")
print(f"Total turns: {len(conversation_json)}")
print(f"Total iterations: {completed_iterations}")
