import os
from typing import List, Optional
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class LineItem(BaseModel):
    description: str = Field(description="Name or service description of the item.")
    quantity: float = Field(description="Numerical quantity billed.")
    unit_price: float = Field(description="Price per individual unit.")
    total_amount: float = Field(description="Total computed amount for the line item.")

class ContractAuditSchema(BaseModel):
    contract_id: Optional[str] = Field(default=None, description="Unique contract or invoice ID.")
    effective_date: Optional[str] = Field(default=None, description="Effective date in YYYY-MM-DD format.")
    vendor_name: str = Field(description="Legal entity name of the vendor.")
    line_items: List[LineItem] = Field(description="Extracted list of all line items.")
    total_contract_value: float = Field(description="Final total monetary value.")
    audit_quote: str = Field(description="Exact verbatim excerpt from PDF proving total contract value.")

def process_pdf_contract_audit(pdf_file_path: str) -> ContractAuditSchema:
    """
    Ingests a raw multi-page PDF document, extracts structured audit data 
    using Gemini 4 Argon with guaranteed schema adherence and explicit thinking controls.
    """
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    print(f"Uploading document: {pdf_file_path} to Gemini File API...")
    uploaded_file = client.files.upload(file=pdf_file_path)

    system_rules = """
    You are an Enterprise Legal & Financial Document Auditor.
    OPERATIONAL RULES:
    1. Extract data ONLY from the attached PDF document. Do NOT guess or infer.
    2. If a non-required field is missing from the text, return null.
    3. Include exact verbatim text in audit_quote to justify extracted values.
    """

    prompt = """
    Inspect the attached PDF contract/invoice and extract all structured fields 
    in accordance with the requested schema. Ensure every line item is captured.
    """

    config = types.GenerateContentConfig(
        system_instruction=system_rules,
        response_mime_type="application/json",
        response_schema=ContractAuditSchema,
        thinking_config=types.ThinkingConfig(
            thinking_level="LOW"
        )
    )

    print("Executing extraction pipeline with Gemini 4 Argon (Thinking Level: LOW)...")
    
    try:
        response = client.models.generate_content(
            model="gemini-4-argon",
            contents=[uploaded_file, prompt],
            config=config
        )
    finally:
        client.files.delete(name=uploaded_file.name)

    if not response.text:
        raise ValueError(f"No response text returned (prompt_feedback={response.prompt_feedback}).")

    audit_result = ContractAuditSchema.model_validate_json(response.text)
    return audit_result

if __name__ == "__main__":
    sample_pdf = "sample_enterprise_contract.pdf"
    if not os.path.exists(sample_pdf):
        raise SystemExit(f"Sample file not found: {sample_pdf}. Add a contract PDF and rerun.")

    result = process_pdf_contract_audit(sample_pdf)
    print("\n--- EXTRACTED AUDIT JSON ---")
    print(result.model_dump_json(indent=2))
