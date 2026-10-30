import os
import json
from google import genai
from google.genai import types

def execute_cyber_threat_triage(source_code_path: str, telemetry_log_path: str):
    """
    Deploys Gemini 4 Carbon to analyze source code alongside system logs,
    identify CWE vulnerabilities, and evaluate exploitability.
    """
    client = genai.Client(
        api_key=os.getenv("GEMINI_FAIRWIND_API_KEY"),
        enterprise=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location="global"
    )

    with open(source_code_path, "r") as code_file:
        source_code = code_file.read()

    with open(telemetry_log_path, "r") as log_file:
        telemetry_logs = log_file.read()

    system_rules = """
    You are Gemini 4 Carbon, an autonomous Cyber Defense Analysis Agent.
    
    OPERATIONAL MANDATES:
    1. Identify all CWE vulnerabilities present in the provided source code.
    2. Cross-reference vulnerabilities with the provided runtime log trace.
    3. Output findings as a structured JSON security report.
    4. Provide a defensive containment strategy for each confirmed flaw.
    """

    prompt = f"""
    SOURCE CODE TO AUDIT:
    ```c
    {source_code}
    ```

    RUNTIME TELEMETRY TRACE:
    ```json
    {telemetry_logs}
    ```

    Perform deep static/dynamic correlation and return the security analysis.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_rules,
        temperature=0.0,
        response_mime_type="application/json",
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH"
        )
    )

    print("Launching Gemini 4 Carbon Security Audit Pipeline...")

    response = client.models.generate_content(
        model="gemini-4-carbon",
        contents=prompt,
        config=config
    )

    print("\n=== GEMINI 4 CARBON SECURITY REPORT ===")
    print(response.text)

if __name__ == "__main__":
    sample_code = "vulnerable_server.c"
    sample_logs = "trace_log.json"

    if os.path.exists(sample_code) and os.path.exists(sample_logs):
        execute_cyber_threat_triage(sample_code, sample_logs)
