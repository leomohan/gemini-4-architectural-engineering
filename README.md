# Architectural Engineering & Security: Google Gemini 4 Argon and Carbon

Welcome to the official companion code repository for the book **Architectural Engineering & Security: Google Gemini 4 Argon and Carbon** by **Mohan Krishnamurthy**.

This repository contains the Python SDK scripts, Pydantic extraction schemas, security triage harnesses, and cost-optimization gateway wrappers presented throughout the ebook.

## 📁 Repository Structure

- `chapter-02-thinking-controls/`
  - `thinking_controls_demo.py`: Programmatic configuration of Low, Medium, and High reasoning tiers.
  - `openai_compatibility_layer.py`: Using Gemini 4 models via the OpenAI SDK wrapper.
- `chapter-03-argon-engineering/`
  - `autonomous_refactoring_agent.py`: Antigravity Managed Agent pipeline for C/C++ to Rust refactoring and SIMD optimization. Takes a Git repository URL, because the agent runs in a remote sandbox.
- `chapter-04-multimodal-extraction/`
  - `contract_audit_extractor.py`: Native PDF ingestion and schema-enforced JSON audit extraction.
- `chapter-05-carbon-cyber-defense/`
  - `threat_triage_pipeline.py`: Cyber threat triage and telemetry correlation with Gemini 4 Carbon.
- `chapter-06-patch-remediation/`
  - `automated_patching_harness.py`: Generating minimal, root-cause unified Git diff patches.
- `chapter-07-safety-frameworks/`
  - `safeguarded_pipeline.py`: Mitigating Indirect Prompt Injection (IPI) using strict isolation rules.
- `chapter-08-enterprise-gateway/`
  - `cost_optimized_gateway.py`: Implicit context caching wrapper with per-request cost accounting, including thinking tokens.

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
   export GEMINI_API_KEY="your-gemini-api-key"
   ```

4. **Add sample inputs:** Chapters 4, 5, and 6 read input files that are not included in this repository. Each script names the file it expects and exits with a message if it is missing. Chapter 6 must run from the root of the target Git repository.

## 🔐 Gemini 4 Carbon Access (Chapters 5 and 6)

Carbon is limited to approved [Fairwind Program](https://deepmind.google/fairwind-program/) partners, and Google has not published a public model ID. Without approved access, these two scripts cannot run. Approved partners authenticate with Application Default Credentials and set the model ID they were given:

```bash
gcloud auth application-default login
export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
export GEMINI_CARBON_MODEL="your-carbon-model-id"
```
