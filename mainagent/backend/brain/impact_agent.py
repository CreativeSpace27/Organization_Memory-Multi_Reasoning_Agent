from openai import OpenAI
from config.settings import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL, LM_STUDIO_API_KEY


class ImpactAgent:

  def __init__(self):
    self.client = OpenAI(
      base_url=LM_STUDIO_BASE_URL,
      api_key=LM_STUDIO_API_KEY
    )

  def analyze(self, question, context):

    prompt = f"""
You are an AI system architect.

Context:
{context}

User question:
{question}

Explain in natural language what will happen if this decision is changed.
Describe system impact clearly.
Do not use bullet points.
"""

    response = self.client.chat.completions.create(
        model=LM_STUDIO_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=120,
        temperature=0.3
    )

    return response.choices[0].message.content