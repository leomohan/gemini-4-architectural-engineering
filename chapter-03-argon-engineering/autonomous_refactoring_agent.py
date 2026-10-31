import os
import time
from google import genai

def run_autonomous_refactoring_agent(
    repo_url: str,
    task_description: str,
    max_total_tokens: int = 2_000_000
) -> str:
    """
    Spawns the Antigravity Managed Agent, powered by Gemini 4 Argon, in a remote
    sandbox to clone, refactor, and debug a Git repository. The agent cannot see
    local paths, so the repository is supplied as a source of the environment.
    Private repositories also need a credential in the environment's network allowlist.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    target_path = "/workspace/repo"

    prompt = f"""
    You are a Principal Software Engineering Agent powered by Gemini 4 Argon.
    Your objective is to refactor legacy code, optimize performance, and eliminate bugs.

    OPERATIONAL MANDATES:
    1. Always establish a performance baseline before making code changes.
    2. Write reproducible verification scripts (cargo test / gtest).
    3. Iterate in a tight loop until all tests pass with zero regressions.
    4. Log build flags, environment quirks, and lessons learned into AGENTS.md.

    TARGET REPOSITORY: {target_path}
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

    interaction = client.interactions.create(
        agent="antigravity-preview-09-2026",
        input=prompt,
        environment={
            "type": "remote",
            "sources": [
                {"type": "repository", "source": repo_url, "target": target_path}
            ]
        },
        agent_config={
            "type": "antigravity",
            "model": "gemini-4-argon",
            "max_total_tokens": max_total_tokens
        },
        background=True
    )

    while interaction.status in ("in_progress", "queued"):
        time.sleep(5)
        interaction = client.interactions.get(id=interaction.id)

    elapsed_time = time.time() - start_time

    if interaction.status != "completed":
        raise RuntimeError(
            f"Agent stopped with status '{interaction.status}' after {elapsed_time:.2f} seconds."
        )

    print(interaction.output_text)
    print(f"\n\nAgent run completed in {elapsed_time:.2f} seconds.")
    print(f"Review its report and files in environment {interaction.environment_id} before merging.")

    return interaction.output_text

if __name__ == "__main__":
    migration_task = """
    Refactor src/crypto/aes_legacy.c to safe Rust in src/crypto/aes_safe.rs.
    Ensure SIMD auto-vectorization is enabled and run performance benchmarks
    against the legacy baseline using 'cargo bench'.
    """
    run_autonomous_refactoring_agent(
        repo_url="https://github.com/your-org/security-core",
        task_description=migration_task
    )
