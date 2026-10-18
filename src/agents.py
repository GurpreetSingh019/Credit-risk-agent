import os
import json
from dotenv import load_dotenv
from pydantic import BaseModel
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class FinancialMetrics(BaseModel):
    current_asset: float
    current_liabilities: float
    total_dept: float
    total_equity: float
    ebit: float
    interest_expense: float
    total_assests: float
    retained_earning: float
    total_revenue: float
def run_extractor_agent(content_text:str)-> dict:
    promt = f"""
    You are a Finacial data extractor.Read The finacial text below and extract the exact numbers.
    Return ONLY a vaild JSON object matching these exact keys:
    {list(FinancialMetrics.model_fields.keys())}
    if a number is missing, use 0.0
    TEXT:
    {content_text}"""
    response = client.chat.completions.create(
        model ="openai/gpt-oss-120b",
        messages=[{"role":"user","content":promt}],
        temperature=0.0

    )
    raw_json = json.loads(response.choices[0].message.content)
    validated_data = FinancialMetrics(**raw_json)
    return validated_data.model_dump()
def run_auditor_agent(ratios: dict)-> str:
    autitor_prompt = f"""
    You are a Senior Commercial Bank Credit Officer. 
    Evaluate the borrower's financial health based ONLY on these calculated metrics and flags:
    Financial Data & Ratios:
    - Current Ratio: {ratios['current_ratio']} (Benchmark: > 1.5)
    - Debt-to-Equity Ratio: {ratios['debt_to_equity']} (Benchmark: < 2.0)
    - Interest Coverage Ratio: {ratios['interest_coverage']} (Benchmark: > 3.0)
    - Altman-Z-Score: {ratios['altman_z_score']} (Safe > 2.99, Distress < 1.81)
    - Triggered Risk Flags: {ratios['flags']}
    Write a professional, 3-paragraph Credit Risk Memo following this exact structure:
    Paragraph 1 - Final Underwriting Decision:
    State clearly whether to APPROVE, APPROVE WITH CONDITIONS, or REJECT the commercial loan application, and summarize the main reason why.
    Paragraph 2 - Ratio Analysis:
    Explain what the calculated Current Ratio, Debt-to-Equity Ratio, Interest Coverage, and Altman Z-Score reveal about the company's liquidity and solvency. Cite the exact numbers provided above.
    Paragraph 3 - Key Risk Flags & Covenants:
    Highlight any specific risk flags triggered in the data and recommend 1-2 protective loan covenants (conditions) the bank should enforce."""
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role":"user","content": autitor_prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content
