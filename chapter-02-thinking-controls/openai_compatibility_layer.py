import os
from openai import OpenAI

# Point client to the Gemini OpenAI-compatible endpoint
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-4-argon",
    messages=[
        {"role": "system", "content": "You are a senior principal cloud architect."},
        {"role": "user", "content": "Design a resilient multi-region enterprise failover architecture."}
    ],
    extra_body={
        "reasoning_effort": "high"
    }
)

print(response.choices[0].message.content)
