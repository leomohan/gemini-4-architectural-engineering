import os
from google import genai
from google.genai import types

# Initialize the Gemini Client
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    enterprise=True,
    project=os.getenv("GOOGLE_CLOUD_PROJECT"),
    location="global"
)

def run_deep_reasoning_task(prompt_text: str, reasoning_tier: str = "HIGH"):
    """
    Executes a high-capacity task using Gemini 4 Argon with long-decode capabilities
    and explicit thinking levels.
    """
    valid_levels = ["LOW", "MEDIUM", "HIGH"]
    if reasoning_tier.upper() not in valid_levels:
        raise ValueError(f"Invalid level. Argon requires one of: {valid_levels}")

    config = types.GenerateContentConfig(
        temperature=0.2,
        max_output_tokens=262144,
        thinking_config=types.ThinkingConfig(
            thinking_level=reasoning_tier.upper()
        )
    )

    print(f"Submitting job with Thinking Level: {reasoning_tier.upper()}...")

    response_stream = client.models.generate_content_stream(
        model="gemini-4-argon",
        contents=prompt_text,
        config=config
    )

    full_response = []
    for chunk in response_stream:
        if hasattr(chunk, "text") and chunk.text:
            print(chunk.text, end="", flush=True)
            full_response.append(chunk.text)

    return "".join(full_response)

if __name__ == "__main__":
    complex_prompt = """
    Ingest the following kernel memory management module (C++) and refactor it into 
    memory-safe, lock-free Rust code using atomic primitives. Conduct a full safety audit
    in your thinking process before emitting the code.
    """
    run_deep_reasoning_task(complex_prompt, reasoning_tier="HIGH")
