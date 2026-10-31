import os
import time
from datetime import date
from typing import Dict, Any, Optional
from google import genai
from google.genai import types

INTRODUCTORY_PRICING_END = date(2026, 11, 30)

class GeminiEnterpriseGateway:
    """
    Production API Gateway for Gemini 4 Argon and Carbon.
    Optimizes context caching layout and calculates per-request billing.
    """
    def __init__(self, is_introductory_pricing: Optional[bool] = None):
        self.client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        if is_introductory_pricing is None:
            is_introductory_pricing = date.today() <= INTRODUCTORY_PRICING_END
        
        if is_introductory_pricing:
            self.input_rate = 2.00
            self.output_rate = 10.00
            self.cached_input_rate = 0.10
        else:
            self.input_rate = 4.00
            self.output_rate = 20.00
            self.cached_input_rate = 0.20

    def execute_cached_engineering_task(
        self, 
        model_name: str, 
        static_codebase_context: str, 
        dynamic_user_query: str,
        thinking_level: str = "MEDIUM"
    ) -> Dict[str, Any]:
        """
        Structures prompts to maximize implicit context caching hits and
        returns response content alongside exact dollar cost metrics.
        """
        system_instruction = """
        You are a Principal Enterprise Systems Engineer. 
        Analyze provided code bases accurately, write memory-safe code, and follow best practices.
        """

        contents = [
            f"STATIC CODEBASE CONTEXT:\n{static_codebase_context}",
            f"DYNAMIC TASK INSTRUCTION:\n{dynamic_user_query}"
        ]

        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            max_output_tokens=65536,
            thinking_config=types.ThinkingConfig(
                thinking_level=thinking_level.upper()
            )
        )

        start_time = time.time()
        
        response = self.client.models.generate_content(
            model=model_name,
            contents=contents,
            config=config
        )
        
        execution_time = time.time() - start_time

        usage = response.usage_metadata
        prompt_tokens = getattr(usage, "prompt_token_count", 0) or 0
        cached_tokens = getattr(usage, "cached_content_token_count", 0) or 0
        uncached_prompt_tokens = max(0, prompt_tokens - cached_tokens)
        candidates_tokens = getattr(usage, "candidates_token_count", 0) or 0
        # Thinking is reported separately from candidates but billed at the output rate
        thinking_tokens = getattr(usage, "thoughts_token_count", 0) or 0
        output_tokens = candidates_tokens + thinking_tokens

        uncached_input_cost = (uncached_prompt_tokens / 1_000_000) * self.input_rate
        cached_input_cost = (cached_tokens / 1_000_000) * self.cached_input_rate
        output_cost = (output_tokens / 1_000_000) * self.output_rate
        total_request_cost = uncached_input_cost + cached_input_cost + output_cost

        return {
            "response_text": response.text,
            "metrics": {
                "execution_time_seconds": round(execution_time, 2),
                "uncached_input_tokens": uncached_prompt_tokens,
                "cached_input_tokens": cached_tokens,
                "thinking_tokens": thinking_tokens,
                "output_and_thinking_tokens": output_tokens,
                "calculated_cost_usd": round(total_request_cost, 6)
            }
        }

if __name__ == "__main__":
    gateway = GeminiEnterpriseGateway()

    large_repo_context = "// [Imagine 100,000 lines of C++ kernel code here...]\n" * 1000
    user_task = "Identify any memory leak risks in the buffer allocation handlers."

    print("Submitting request through Enterprise Gateway...")
    result = gateway.execute_cached_engineering_task(
        model_name="gemini-4-argon",
        static_codebase_context=large_repo_context,
        dynamic_user_query=user_task,
        thinking_level="HIGH"
    )

    print("\n=== EXECUTION METRICS & COST AUDIT ===")
    for key, val in result["metrics"].items():
        print(f"{key}: {val}")
