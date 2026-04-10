from openai import OpenAI
from config.settings import LM_STUDIO_BASE_URL, LM_STUDIO_MODEL, LM_STUDIO_API_KEY


class ReasoningAgent:

    def __init__(self):
        self.client = OpenAI(
            base_url=LM_STUDIO_BASE_URL,
            api_key=LM_STUDIO_API_KEY
        )

    def reason(self, question, context):

        prompt = f"""
You are an AI that explains engineering decisions in natural language.

Context:
{context}

User question:
{question}

Write a clear natural explanation.
Do NOT return bullet points.
Do NOT list fields.
Explain like a human explaining to a teammate.
"""

        try:
            response = self.client.chat.completions.create(
                model=LM_STUDIO_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=120,
                temperature=0.3
            )

            return response.choices[0].message.content

        except:
            return context