import json
import httpx
import os
from pathlib import Path
import re

API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable is not set")
MODEL = "gemini-2.5-pro"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def _extract_json(text: str) -> str:
    # Remove markdown code blocks
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        return match.group(1).strip()
    
    # Try finding raw json object or array
    text = text.strip()
    start_obj = text.find("{")
    end_obj = text.rfind("}")
    start_arr = text.find("[")
    end_arr = text.rfind("]")
    
    start = -1
    end = -1
    
    if start_obj != -1 and end_obj != -1 and start_arr != -1 and end_arr != -1:
        if start_obj < start_arr:
            start, end = start_obj, end_obj
        else:
            start, end = start_arr, end_arr
    elif start_obj != -1 and end_obj != -1:
        start, end = start_obj, end_obj
    elif start_arr != -1 and end_arr != -1:
        start, end = start_arr, end_arr
        
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
        
    return text

def main():
    prompts = [
        "US-33_prompt.txt",
        "US-35_prompt.txt",
        "US-36_prompt.txt"
    ]
    
    prompt_dir = Path("srs_docs/ready_prompts")
    review_dir = Path("reviews")
    review_dir.mkdir(exist_ok=True)
    
    instruction_prepend = "Evaluate this document strictly following its internal instructions. Return ONLY the JSON result. No markdown formatted code blocks, no conversational text. Just the `{}` or `[]` JSON."

    for prompt_file in prompts:
        prompt_name = prompt_file.replace("_prompt.txt", "")
        prompt_path = prompt_dir / prompt_file
        out_file = review_dir / f"{prompt_name}_review.json"
        
        print(f"Processing {prompt_name}...")
        prompt_text = prompt_path.read_text(encoding="utf-8")
        
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"{instruction_prepend}\n\n{prompt_text}"}]
                }
            ],
            "generationConfig": {
                "temperature": 0
            }
        }
        
        try:
            with httpx.Client(timeout=300) as client:
                response = client.post(URL, json=payload)
                
            if response.status_code != 200:
                print(f"Error {response.status_code}: {response.text}")
                continue
                
            data = response.json()
            try:
                content = data["candidates"][0]["content"]["parts"][0]["text"]
                json_content = _extract_json(content)
                out_file.write_text(json_content, encoding="utf-8")
                print(f"Successfully saved {prompt_name} review ({len(json_content)} chars).")
            except KeyError as e:
                print(f"Failed to parse response for {prompt_name}: {e}")
                print(data)
                
        except Exception as e:
            print(f"Exception for {prompt_name}: {e}")

if __name__ == "__main__":
    main()
