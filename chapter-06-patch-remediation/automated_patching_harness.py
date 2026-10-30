import os
from google import genai
from google.genai import types

def run_automated_patching_pipeline(vulnerable_file_path: str, crash_report_path: str):
    """
    Ingests a vulnerable C/C++ source file and crash log, deploys Gemini 4 Carbon
    to generate a minimal root-cause Git diff patch, and verifies the solution.
    """
    client = genai.Client(
        api_key=os.getenv("GEMINI_FAIRWIND_API_KEY"),
        enterprise=True,
        project=os.getenv("GOOGLE_CLOUD_PROJECT"),
        location="global"
    )

    with open(vulnerable_file_path, "r") as f:
        source_code = f.read()

    with open(crash_report_path, "r") as f:
        crash_log = f.read()

    system_rules = """
    You are Gemini 4 Carbon, an automated Cyber Defense Remediation Agent.
    
    OPERATIONAL MANDATES:
    1. Analyze the source code and crash log to identify the root cause of the memory flaw.
    2. Write a minimal, idiomatic, high-fidelity security patch.
    3. Ensure zero API breaking changes or functional regressions.
    4. Return ONLY a valid unified Git diff block (```diff ... ```) containing the patch.
    """

    prompt = f"""
    TARGET SOURCE CODE ({vulnerable_file_path}):
    ```cpp
    {source_code}
    ```

    SANITIZER / CRASH LOG:
    ```text
    {crash_log}
    ```

    Generate a secure root-cause patch in unified Git diff format.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_rules,
        temperature=0.0,
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH"
        )
    )

    print("Submitting vulnerability to Gemini 4 Carbon Patch Engine...")

    response = client.models.generate_content(
        model="gemini-4-carbon",
        contents=prompt,
        config=config
    )

    patch_diff = response.text
    print("\n=== GENERATED UNIFIED GIT DIFF ===")
    print(patch_diff)

    patch_file = "security_remediation.patch"
    with open(patch_file, "w") as f:
        f.write(patch_diff)

    print(f"\nPatch saved successfully to {patch_file}. Ready for automated git apply & CI testing.")

if __name__ == "__main__":
    vulnerable_src = "src/v8_buffer_parser.cc"
    sanitizer_log = "logs/asan_crash_uaf.log"

    if os.path.exists(vulnerable_src) and os.path.exists(sanitizer_log):
        run_automated_patching_pipeline(vulnerable_src, sanitizer_log)
