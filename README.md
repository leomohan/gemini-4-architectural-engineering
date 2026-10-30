# Architectural Engineering & Security: Google Gemini 4 Argon and Carbon

Welcome to the official companion code repository for the book **Architectural Engineering & Security: Google Gemini 4 Argon and Carbon** by **Mohan Krishnamurthy**.

This repository contains all production-ready Python SDK scripts, Pydantic extraction schemas, security triage harnesses, and cost-optimization gateway wrappers presented throughout the ebook.

## 📁 Repository Structure

- `chapter-02-thinking-controls/`
  - `thinking_controls_demo.py`: Programmatic configuration of Low, Medium, and High reasoning tiers.
  - `openai_compatibility_layer.py`: Using Gemini 4 models via the OpenAI SDK wrapper.
- `chapter-03-argon-engineering/`
  - `autonomous_refactoring_agent.py`: Managed Agent pipeline for C/C++ to Rust refactoring and SIMD optimization.
- `chapter-04-multimodal-extraction/`
  - `contract_audit_extractor.py`: Native PDF ingestion and schema-enforced JSON audit extraction.
- `chapter-05-carbon-cyber-defense/`
  - `threat_triage_pipeline.py`: Cyber threat triage and telemetry correlation with Gemini 4 Carbon.
- `chapter-06-patch-remediation/`
  - `automated_patching_harness.py`: Generating minimal, root-cause unified Git diff patches.
- `chapter-07-safety-frameworks/`
  - `safeguarded_pipeline.py`: Mitigating Indirect Prompt Injection (IPI) using strict isolation rules.
- `chapter-08-enterprise-gateway/`
  - `cost_optimized_gateway.py`: Implicit context caching wrapper with exact request cost accounting.

## 🚀 Quickstart

1. **Clone the repository:**
   ```bash
   git clone https://github.com/leomohan/gemini-4-architectural-engineering.git
   cd gemini-4-architectural-engineering
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   ```bash
   export GEMINI_API_KEY="your-api-key"
   export GEMINI_FAIRWIND_API_KEY="your-fairwind-partner-key"
   export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
   ```
