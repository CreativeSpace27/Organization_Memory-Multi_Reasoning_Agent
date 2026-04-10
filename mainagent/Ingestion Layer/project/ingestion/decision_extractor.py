
import json
import re
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# 🔥 Connect to LM Studio
llm = ChatOpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio",
    model="google/gemma-3-1b",
    temperature=0,
    max_tokens=1000 
)

# 🧾 Prompt Template
prompt = PromptTemplate(
    input_variables=["chunk"],
    template="""
TASK: Extract decision JSON.
INSTRUCTION: Be extremely concise in your internal reasoning. Do not over-analyze. 
Once you identify the decision, output the JSON immediately.

FORMAT:
{{
  "decision": "...",
  "reasoning": ["..."],
  "alternatives": ["..."],
  "sources":["..."],
  "impacts": ["..."]
  
}}

TEXT:
{chunk}
"""
)

def extract_decision(chunk):
    try:
        print("🚀 Sending chunk to LLM...")
        formatted_prompt = prompt.format(chunk=chunk)
        response = llm.invoke(formatted_prompt)
        content = response.content.strip()

        # 1. REMOVE DEEPSEEK THINKING BLOCK
        # This removes everything between <think> and </think>
        content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()

        # 2. FIND THE JSON BLOCK
        # We look for the JSON at the end of the string
        match = re.search(r"(\{.*\})", content, re.DOTALL)

        if match:
            json_text = match.group(1).strip()
            # Remove any markdown garbage
            json_text = json_text.replace("```json", "").replace("```", "").strip()
            
            try:
                data = json.loads(json_text)
                # Ensure the AI actually found a decision
                if not data.get("decision"):
                    print("⚠️ AI found no decision in this text.")
                return data
            except json.JSONDecodeError:
                print("⚠️ JSON still malformed after cleaning.")
        
        print("🛠 No valid JSON found. Using fallback...")
        return fallback_parse(content)

    except Exception as e:
        print(f"❌ Extraction Error: {e}")
        return None

def fix_json(text):
    """Fixes common trailing commas or single quotes."""
    text = text.replace("'", '"')
    text = re.sub(r",\s*\}", "}", text)
    text = re.sub(r",\s*\]", "]", text)
    return text

def fallback_parse(text):
    """Simple extraction if the LLM fails to provide valid JSON."""
    return {
        "decision": "Manual Check Required", 
        "reasoning": ["Could not parse structured output"], 
        "alternatives": []
    }




