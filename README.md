# 🏦 Autonomous Commercial Credit Due-Diligence Agent

An end-to-end **Multi-Agent Financial RAG System** that automates corporate loan underwriting. Upload an audited SEC Form 10-K or financial report (PDF) to extract key balance sheet figures, compute deterministic solvency and liquidity ratios, flag covenant breaches, and generate an executive Credit Risk Memo in seconds.

---

## 🎯 Why This Project Matters
Standard Large Language Models (LLMs) suffer from context retrieval errors and **arithmetic hallucinations** when analyzing 100+ page financial filings. In commercial banking, a small calculation error can lead to millions in defaulted loans.

This project solves that problem by **decoupling unstructured data extraction from mathematical computation**:
1. **Semantic Retrieval (RAG):** Uses `PyPDF` and `ChromaDB` to chunk filings and retrieve only the relevant Consolidated Balance Sheet and Income Statement sections.
2. **Structured Entity Extraction (Agent 1):** Uses `Groq (Llama-3.3-70B)` enforced by `Pydantic` schemas to extract 9 core audited figures into strict JSON.
3. **Deterministic Math Engine:** Uses pure Python (`calculator.py`) to compute exact financial ratios with zero hallucination risk.
4. **Automated Credit Underwriter (Agent 2):** Evaluates calculated ratios and warning flags to write a structured, 3-paragraph **Credit Risk Memo**.

---

## 📊 Financial Metrics & Benchmarks Computed
* **Current Ratio (Liquidity):** $\frac{\text{Current Assets}}{\text{Current Liabilities}}$ *(Healthy Benchmark: $\ge 1.5$)*
* **Debt-to-Equity Ratio (Leverage):** $\frac{\text{Total Debt}}{\text{Total Equity}}$ *(Healthy Benchmark: $\le 2.0$)*
* **Interest Coverage Ratio:** $\frac{\text{Operating Income (EBIT)}}{\text{Interest Expense}}$ *(Healthy Benchmark: $\ge 3.0$)*
* **Altman Z-Score (Bankruptcy Predictor):** Evaluates working capital, retained earnings, operating efficiency, and leverage to classify companies into **Safe ($> 2.99$)**, **Grey ($1.81 - 2.99$)**, or **Distress ($< 1.81$)** zones.

---

## 🛠️ Tech Stack
* **Language:** Python 3.10+
* **LLM & Orchestration:** Groq Cloud API (`llama-3.3-70b-versatile`), Pydantic (Structured Outputs)
* **RAG & Vector Database:** ChromaDB, PyPDF
* **Frontend UI:** Streamlit
* **Security:** Python-dotenv

---

## 📂 Project Structure
```text
credit-risk-agent/
├── src/
│   ├── ingestion.py     # PDF text extraction, chunking, and ChromaDB vector search
│   ├── agents.py        # Pydantic schema, JSON Extractor Agent, and Risk Auditor Agent
│   └── calculator.py    # Deterministic financial ratio & Altman Z-Score engine
├── app.py               # Interactive Streamlit web dashboard
├── requirements.txt     # Project dependencies
├── .gitignore           # Excludes venv/ and .env from version control
└── README.md            # Project documentation
```

---

## 🚀 How to Run Locally

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/credit-risk-due-diligence-agent.git
cd credit-risk-due-diligence-agent
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Your API Key
Create a `.env` file in the root directory and add your free Groq API key:
```env
GROQ_API_KEY=gsk_your_secret_api_key_here
```

### 5. Launch the App
```bash
streamlit run app.py
```