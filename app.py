import streamlit as st
from src.ingestion import extract_and_chunk_pdf,store_and_retrive_financials
from src.agents import run_extractor_agent,run_auditor_agent
from src.calculator import calculator_ration

st.set_page_config(page_title ="AI Credit Underwriter",layout="wide")
st.title("Credit Risk Agent")
st.write("An automated financial due-diligence agent that parses corporate PDF filings, accurately computes credit and bankruptcy ratios, "
        "and generates professional loan approval memos in seconds")

uploaded_file = st.file_uploader("Upload Annual Report / 10-k (PDF)", type = ["pdf"])
if uploaded_file is not None:
    with open("temp_report.pdf","wb") as f:
        f.write(uploaded_file.getbuffer())
    if st.button("Run Autonomus Credit Audit"):
        with st.spinner("1/3 Reading PDF and Searching Vector database..."):
            chunks = extract_and_chunk_pdf("temp_report.pdf")
            relevant_text = store_and_retrive_financials(chunks)
        with st.spinner("2/3 Extracting Audited Figures & Computing Ratios..."):
            raw_metrics = run_extractor_agent(relevant_text)
            computed = calculator_ration(raw_metrics)
        with st.spinner("3/3 Drafting Executive Credit Risk Memo..."):
            memo = run_auditor_agent(computed)
        
        st.subheader("1. Deterministic Financial Ratios")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Current Ratio", computed["current_ratio"]) 
        col2.metric("Debt to equity",computed["debt_to_equity"])
        col3.metric("Interest_coverage",computed["interest_coverage"])
        col4.metric("Altman Z Score", computed["altman_z_score"])

        st.subheader("2. Automated Risk Flags")
        for flag in computed["flags"]:
            st.error(flag)
        st.subheader("3. Executive Credit Risk Memo")
        st.write(memo)

