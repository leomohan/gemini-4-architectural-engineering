import os
import time
from google import genai
from google.genai import types

def run_autonomous_refactoring_agent(repo_path: str, task_description: str):
    """
    Spawns a Gemini 4 Argon Managed Agent to autonomously analyze,
    refactor, and debug a local code repository.
    """
    client = genai.Client(
        api_key=os.getenv("GEMINI_API_KEY"),
        enterprise=True
    )

    system_instruction = """
    You are a Principal Software Engineering Agent powered by Gemini 4 Argon.
    Your objective is to refactor legacy code, optimize performance, and eliminate bugs.
    
    OPERATIONAL MANDATES:
    1. Always establish a performance baseline before making code changes.
    2. Write reproducible verification scripts (cargo test / gtest).
    3. Iterate in a tight loop until all tests pass with zero regressions.
    4. Log build flags, environment quirks, and lessons learned into AGENTS.md.
    """

    config = types.GenerateContentConfig(
        temperature=0.1,
        max_output_tokens=1048576,
        system_instruction=system_instruction,
        thinking_config=types.ThinkingConfig(
            thinking_level="HIGH"
        )
    )

    prompt = f"""
    TARGET REPOSITORY: {repo_path}
    TASK ASSIGNMENT: {task_description}

    EXECUTION STEPS:
    Step 1: Scan the directory tree and analyze dependencies.
    Step 2: Run existing benchmarks to record baseline execution speed and memory usage.
    Step 3: Refactor identified C/C++ memory-unsafe modules into idiomatic Rust.
    Step 4: Execute compile checks and fix any compiler or ownership errors in a loop.
    Step 5: Verify that output equivalence matches 100% against the baseline test suite.
    Step 6: Update AGENTS.md with new build skills and final performance metrics.
    """

    print("Launching Gemini 4 Argon Autonomous Refactoring Agent...")
    start_time = time.time()

    response_stream = client.models.generate_content_stream(
        model="gemini-4-argon",
        contents=prompt,
        config=config
    )

    for chunk in response_stream:
        if hasattr(chunk, "text") and chunk.text:
            print(chunk.text, end="", flush=True)

    elapsed_time = time.time() - start_time
    print(f"\n\nRefactoring and verification completed in {elapsed_time:.2f} seconds.")

if __name__ == "__main__":
    migration_task = """
    Refactor src/crypto/aes_legacy.c to safe Rust in src/crypto/aes_safe.rs.
    Ensure SIMD auto-vectorization is enabled and run performance benchmarks 
    against the legacy baseline using 'cargo bench'.
    """
    run_autonomous_refactoring_agent(
        repo_path="/workspace/security-core",
        task_description=migration_task
    )
