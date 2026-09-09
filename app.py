import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import io

st.set_page_config(page_title="Forensic Wealth Desk", layout="wide")
st.title("🏛️ Private Wealth Forensic Desk & Quant Risk Co-Pilot")
st.write("---")

@st.cache_data
def get_baseline_data():
    return pd.DataFrame([
        {"Ticker": "HAL", "Units": 61, "Avg_Cost": 4430.88, "LTP": 5029.00, "ROCE": 38.20, "CCC": 28, "Backlog": "94100 Cr", "Command": "RETAIN_CORE_SOVEREIGN_MOAT"},
        {"Ticker": "BAJAJHFL", "Units": 3700, "Avg_Cost": 104.49, "LTP": 84.01, "ROCE": 7.10, "CCC": 45, "Backlog": "N/A", "Command": "EX_100_HARVEST_VALUE_LOSS"},
        {"Ticker": "EMIL", "Units": 1250, "Avg_Cost": 110.20, "LTP": 136.65, "ROCE": 12.70, "CCC": 84, "Backlog": "N/A", "Command": "RETAIN_CORE_FORTRESS_ANCHOR"},
        {"Ticker": "KPIGREEN", "Units": 600, "Avg_Cost": 438.89, "LTP": 292.05, "ROCE": 30.20, "CCC": 58, "Backlog": "6800 Cr", "Command": "TACTICAL_CONCENTRATION_TRIM"},
        {"Ticker": "SIYARAM", "Units": 7500, "Avg_Cost": 79.91, "LTP": 34.53, "ROCE": 18.40, "CCC": 58, "Backlog": "SME Brass", "Command": "RETAIN_CORE_FORTRESS_ANCHOR"},
        {"Ticker": "ZAGGLE", "Units": 1200, "Avg_Cost": 306.51, "LTP": 180.11, "ROCE": 24.60, "CCC": 65, "Backlog": "SaaS", "Command": "EX_100_HARVEST_VALUE_LOSS"}
    ])

st.sidebar.header("📊 Data Management Console")
uploaded_file = st.sidebar.file_uploader("Upload Broker Statement (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        rename_map = {}
        for col in df.columns:
            col_upper = str(col).upper().strip()
            if col_upper in ["TICKER", "SYMBOL", "STOCK", "COMPANY"]: rename_map[col] = "Ticker"
            elif col_upper in ["UNITS", "QTY", "QUANTITY", "SHARES"]: rename_map[col] = "Units"
            elif col_upper in ["AVG_COST", "BUY_AVG", "AVG COST", "COST"]: rename_map[col] = "Avg_Cost"
            elif col_upper in ["LTP", "LAST PRICE", "CURRENT PRICE", "CMP"]: rename_map[col] = "LTP"
        df.rename(columns=rename_map, inplace=True)
        
        if "Ticker" not in df.columns: df["Ticker"] = "UNKNOWN"
        if "Units" not in df.columns: df["Units"] = 0
        if "Avg_Cost" not in df.columns: df["Avg_Cost"] = 0.0
        if "LTP" not in df.columns: df["LTP"] = 0.0
        
        from report_engine import assign_command, assign_roce, assign_ccc
        df["Command"] = df["Ticker"].apply(assign_command)
        df["ROCE"] = df["Ticker"].apply(assign_roce)
        df["CCC"] = df["Ticker"].apply(assign_ccc)
        df["Backlog"] = df["Ticker"].apply(lambda t: "94100 Cr" if str(t).upper()=="HAL" else "N/A")
        st.sidebar.success("✅ Portfolio Aligned Natively!")
    except Exception as e:
        st.sidebar.error(f"Error parsing file: {e}")
        df = get_baseline_data()
else:
    st.sidebar.info("💡 Running on Synchronized Ground Truth Baseline")
    df = get_baseline_data()

df["Units"] = pd.to_numeric(df["Units"], errors='coerce').fillna(0)
df["Avg_Cost"] = pd.to_numeric(df["Avg_Cost"], errors='coerce').fillna(0.0)
df["LTP"] = pd.to_numeric(df["LTP"], errors='coerce').fillna(0.0)
df["Deployed_Capital"] = df["Units"] * df["Avg_Cost"]
df["Current_Value"] = df["Units"] * df["LTP"]
df["Unrealized_PnL"] = df["Current_Value"] - df["Deployed_Capital"]
df["Delta_ROCE_Spread"] = df["ROCE"] - 11.50

total_deployed = df["Deployed_Capital"].sum()
total_value = df["Current_Value"].sum()
total_pnl = df["Unrealized_PnL"].sum()

exit_cash = df[df["Command"] == "EX_100_HARVEST_VALUE_LOSS"]["Current_Value"].sum()
trim_cash = df[df["Command"] == "TACTICAL_CONCENTRATION_TRIM"]["Current_Value"].sum() * 0.45
cash_unlocked = exit_cash + trim_cash

near_status_quo = total_value * 1.12
med_status_quo = total_value * 1.25
long_status_quo = total_value * 1.50
near_realigned = near_status_quo + 815396.58
med_realigned = med_status_quo + 1296654.00
long_realigned = long_status_quo + 2700000.00

scenario_df = pd.DataFrame({
    "Strategic Tracking Horizon": ["Near-Term Target (3–6 Months)", "Medium-Term Target (12–18 Months)", "Long-Term Target (3–5 Years)"],
    "Path A: Stagnant Status Quo Value": [near_status_quo, med_status_quo, long_status_quo],
    "Path B: Realigned Core Engine Value": [near_realigned, med_realigned, long_realigned],
    "Absolute Strategic Alpha Advantage (Profit)": [815396.58, 1296654.00, 2700000.00]
})

from report_engine import convert_to_excel_stream, get_pdf_html
excel_data = convert_to_excel_stream(df, scenario_df, total_deployed, total_value, total_pnl, cash_unlocked)
pdf_html_content = get_pdf_html(total_deployed, total_value, total_pnl, cash_unlocked, scenario_df, df)

col_btn1, col_btn2 = st.columns(2)
with col_btn1:
    st.download_button(label="📥 Download Unified Excel Report", data=excel_data, file_name="Forensic_Wealth_Master_Audit_Report.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", use_container_width=True)
with col_btn2:
    st.download_button(label="📥 Download Unified PDF Report", data=pdf_html_content.encode('utf-8'), file_name="Forensic_Wealth_Master_Audit_Report.html", mime="text/html", use_container_width=True)

st.write("---")
m_tab1, m_tab2, m_tab3, m_tab4 = st.tabs(["📋 Master Portfolio Ledger", "🚨 Capital Leak Audits", "🎯 Multi-Timeframe Targets", "📈 VC Scenario Room"])

with m_tab1:
    st.subheader("📊 Active Portfolio Ledger Matrix")
    st.dataframe(df.style.format({"Avg_Cost": "₹{:.2f}", "LTP": "₹{:.2f}", "Deployed_Capital": "₹{:.2f}", "Current_Value": "₹{:.2f}", "Unrealized_PnL": "₹{:.2f}", "Delta_ROCE_Spread": "{:+.2f}%"}), use_container_width=True)
with m_tab2:
    st.subheader("🔎 Capital Efficiency & Working Capital Alerts")
    col_leak, col_ccc = st.columns(2)
    with col_leak:
        leaks = df[df["Delta_ROCE_Spread"] < 0]
        if not leaks.empty: st.dataframe(leaks[["Ticker", "ROCE", "Delta_ROCE_Spread", "Command"]], use_container_width=True)
        else: st.success("✅ Zero Capital-Destroying Spread Gaps Detected!")
    with col_ccc:
        traps = df[df["CCC"] > 120]
        if not traps.empty: st.dataframe(traps[["Ticker", "CCC", "Command"]], use_container_width=True)
        else: st.success("✅ All Working Capital Conversion Speeds Healthy!")
with m_tab3:
    st.subheader("🏹 Algorithmic Target Projections")
    target_df = df[["Ticker", "LTP"]].copy()
    target_df["Near_Term_Target (12%)"] = target_df["LTP"] * 1.12
    target_df["Medium_Term_Target (25%)"] = target_df["LTP"] * 1.25
    target_df["Long_Term_Target (50%)"] = target_df["LTP"] * 1.50
    st.dataframe(target_df.style.format({"LTP": "₹{:.2f}", "Near_Term_Target (12%)": "₹{:.2f}", "Medium_Term_Target (25%)": "₹{:.2f}", "Long_Term_Target (50%)": "₹{:.2f}"}), use_container_width=True)
with m_tab4:
    st.subheader("🏛️ Institutional Venture Capital Scenario Board")
    st.dataframe(scenario_df.style.format({"Path A: Stagnant Status Quo Value": "₹{:,.2f}", "Path B: Realigned Core Engine Value": "₹{:,.2f}", "Absolute Strategic Alpha Advantage (Profit)": "+₹{:,.2f}"}), use_container_width=True)
