from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

res = client.chat.completions.create(
    model="deepseek/deepseek-r1-0528-qwen3-8b",
    messages=[{"role": "user", "content": "Say hello"}]
)

print(res.choices[0].message.content)