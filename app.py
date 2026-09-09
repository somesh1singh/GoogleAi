import streamlit as st
import pandas as pd

# Page setup layout configuration
st.set_page_config(page_title="Forensic Wealth Desk", layout="wide")

st.title("🏛️ Private Wealth Forensic Desk & Quant Risk Co-Pilot")
st.write("---")

# 1. HARDCODED BASELINE DATA INGESTION ENGINE (THE DEMO LAYER)
@st.cache_data
def get_baseline_data():
    return pd.DataFrame([
        {"Ticker": "HAL", "Units": 61, "Avg_Cost": 4430.88, "LTP": 5029.00, "ROCE": 38.20, "CCC": 28, "Backlog": "94100 Cr", "Command": "RETAIN_CORE_SOVEREIGN_MOAT"},
        {"Ticker": "BAJAJHFL", "Units": 3700, "Avg_Cost": 104.49, "LTP": 84.01, "ROCE": 7.10, "CCC": 45, "Backlog": "N/A", "Command": "EX_100_HARVEST_SHORT_TERM_LOSS"},
        {"Ticker": "EMIL", "Units": 1250, "Avg_Cost": 110.20, "LTP": 136.65, "ROCE": 12.70, "CCC": 84, "Backlog": "N/A", "Command": "RETAIN_CORE_FORTRESS_ANCHOR"},
        {"Ticker": "KPIGREEN", "Units": 600, "Avg_Cost": 438.89, "LTP": 292.05, "ROCE": 30.20, "CCC": 58, "Backlog": "6800 Cr", "Command": "TACTICAL_TRIM_30_PERCENT"},
        {"Ticker": "SIYARAM", "Units": 7500, "Avg_Cost": 79.91, "LTP": 34.53, "ROCE": 18.40, "CCC": 58, "Backlog": "SME Brass", "Command": "RETAIN_CORE_FORTRESS_ANCHOR"},
        {"Ticker": "ZAGGLE", "Units": 1200, "Avg_Cost": 306.51, "LTP": 180.11, "ROCE": 24.60, "CCC": 65, "Backlog": "SaaS", "Command": "EX_100_HARVEST_SHORT_TERM_LOSS"}
    ])

# 2. DYNAMIC INPUT SIDEBAR LAYER
st.sidebar.header("📊 Data Management Console")
uploaded_file = st.sidebar.file_uploader("Upload Broker Statement (CSV or Excel)", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        # DYNAMIC RECONCILIATION MAPPING LAYER
        rename_map = {}
        for col in df.columns:
            col_upper = str(col).upper().strip()
            if col_upper in ["TICKER", "SYMBOL", "STOCK", "COMPANY"]: rename_map[col] = "Ticker"
            elif col_upper in ["UNITS", "QTY", "QUANTITY", "SHARES"]: rename_map[col] = "Units"
            elif col_upper in ["AVG_COST", "BUY_AVG", "AVG COST", "COST"]: rename_map[col] = "Avg_Cost"
            elif col_upper in ["LTP", "LAST PRICE", "CURRENT PRICE", "CMP"]: rename_map[col] = "LTP"
        df.rename(columns=rename_map, inplace=True)
        
        # INGESTION FALLBACK LAYER
        if "Ticker" not in df.columns: df["Ticker"] = "UNKNOWN"
        if "Units" not in df.columns: df["Units"] = 0
        if "Avg_Cost" not in df.columns: df["Avg_Cost"] = 0.0
        if "LTP" not in df.columns: df["LTP"] = 0.0
        
        # AUTOMATED STRATEGIC COMMAND RULES PIPELINE (THE REALIGNMENT INTELLIGENCE)
        # Dynamically matches tickers to their core strategic track automatically
        def assign_command(ticker):
            t = str(ticker).upper().strip()
            if t in ["ZAGGLE", "ROUTE", "KNRCON", "DCXINDIA", "FINOPB", "BAJAJHFL", "DENISCHEM", "GREENPOWER", "GSFC", "GPPL", "HITECH", "INA", "JAYSREETEA", "MOSCHIP", "PROTEAN", "RAILTEL", "TEXRAIL", "VISAKAIND"]:
                return "EX_100_HARVEST_VALUE_LOSS"
            elif t in ["IREDA", "KPITTECH", "IRFC", "KPIGREEN", "NTPCGREEN", "WAAREEENER", "PFC"]:
                return "TACTICAL_CONCENTRATION_TRIM"
            elif t in ["HAL", "DIXON", "SIYARAM", "EMIL", "TRENT", "TATAMOTORS", "ICICIBANK", "LT", "HDFCBANK", "DMART", "BECTORFOOD", "DATAPATTNS", "GRSE", "BDL", "DLINKINDIA", "GREENPLY", "JSWENERGY", "TATASTEEL", "RELIANCE"]:
                return "RETAIN_CORE_PREMIUM_ANCHOR"
            else:
                return "RETAIN_CORE_COMPOUNDER"
                
        def assign_roce(ticker):
            t = str(ticker).upper().strip()
            roce_map = {"HAL": 38.2, "GRSE": 36.6, "DIXON": 29.2, "KPIGREEN": 30.2, "DATAPATTNS": 28.4, "DLINKINDIA": 28.4, "SIYARAM": 18.4, "KNRCON": 8.4, "DCXINDIA": 6.2, "DENISCHEM": 5.4, "FINOPB": 4.2}
            return roce_map.get(t, 11.50)
            
        def assign_ccc(ticker):
            t = str(ticker).upper().strip()
            ccc_map = {"HAL": 28, "DIXON": 34, "SIYARAM": 58, "EMIL": 84, "ROUTE": 112, "KNRCON": 168}
            return ccc_map.get(t, 60)

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

# 4. FIXED MATHEMATICAL CALCULATION ENGINE
df["Units"] = pd.to_numeric(df["Units"], errors='coerce').fillna(0)
df["Avg_Cost"] = pd.to_numeric(df["Avg_Cost"], errors='coerce').fillna(0.0)
df["LTP"] = pd.to_numeric(df["LTP"], errors='coerce').fillna(0.0)

df["Deployed_Capital"] = df["Units"] * df["Avg_Cost"]
df["Current_Value"] = df["Units"] * df["LTP"]
df["Unrealized_PnL"] = df["Current_Value"] - df["Deployed_Capital"]
df["Delta_ROCE_Spread"] = df["ROCE"] - 11.50

# 5. EXECUTIVE DASHBOARD ROLLUP METRICS
total_deployed = df["Deployed_Capital"].sum()
total_value = df["Current_Value"].sum()
total_pnl = df["Unrealized_PnL"].sum()

# Dynamic math scanning rows to calculate released capital automatically
exit_cash = df[df["Command"] == "EX_100_HARVEST_VALUE_LOSS"]["Current_Value"].sum()
trim_cash = df[df["Command"] == "TACTICAL_CONCENTRATION_TRIM"]["Current_Value"].sum() * 0.45  # Blended 45% trim constant
cash_unlocked = exit_cash + trim_cash

m1, m2, m3, m4 = st.columns(4)
m1.metric("Deployed Capital Base", f"₹{total_deployed:,.2f}")
m2.metric("Active Portfolio Value", f"₹{total_value:,.2f}")
m3.metric("Net Unrealized Delta P&L", f"₹{total_pnl:,.2f}", delta=f"{((total_pnl/total_deployed)*100 if total_deployed > 0 else 0):.2f}%", delta_color="inverse")
m4.metric("Unlocked STP Liquidity", f"₹{cash_unlocked:,.2f}")

st.write("---")

# 6. TABULAR INTERACTIVE AUDIT WORKSPACE
tab1, tab2, tab3 = st.tabs(["📋 Master Portfolio Ledger", "🚨 Capital Leak Audits", "🎯 Multi-Timeframe Targets"])

with tab1:
    st.subheader("📊 51-Stock Active Forensic Ledger Matrix")
    st.dataframe(df.style.format({
        "Avg_Cost": "₹{:.2f}", "LTP": "₹{:.2f}", "Deployed_Capital": "₹{:.2f}", 
        "Current_Value": "₹{:.2f}", "Unrealized_PnL": "₹{:.2f}", "Delta_ROCE_Spread": "{:+.2f}%"
    }), use_container_width=True)

with tab2:
    st.subheader("🔎 Capital Efficiency & Working Capital Alerts")
    col_leak, col_ccc = st.columns(2)
    
    with col_leak:
        st.write("🔴 **Negative-Spread Capital Leaks (ROCE < 11.5%)**")
        leaks = df[df["Delta_ROCE_Spread"] < 0]
        if not leaks.empty:
            st.dataframe(leaks[["Ticker", "ROCE", "Delta_ROCE_Spread", "Command"]], use_container_width=True)
        else:
            st.success("✅ Zero Capital-Destroying Spread Gaps Detected!")
            
    with col_ccc:
        st.write("⚠️ **Working Capital Traps (Cash Conversion Cycle > 120 Days)**")
        traps = df[df["CCC"] > 120]
        if not traps.empty:
            st.dataframe(traps[["Ticker", "CCC", "Command"]], use_container_width=True)
        else:
            st.success("✅ All Working Capital Conversion Speeds Healthy!")

with tab3:
    st.subheader("🏹 Algorithmic Target Projections & Exit Floors")
    target_df = df[["Ticker", "LTP"]].copy()
    target_df["Near_Term_Target (12%)"] = target_df["LTP"] * 1.12
    target_df["Medium_Term_Target (25%)"] = target_df["LTP"] * 1.25
    target_df["Long_Term_Target (50%)"] = target_df["LTP"] * 1.50
    
    st.dataframe(target_df.style.format({
        "LTP": "₹{:.2f}", "Near_Term_Target (12%)": "₹{:.2f}", 
        "Medium_Term_Target (25%)": "₹{:.2f}", "Long_Term_Target (50%)": "₹{:.2f}"
    }), use_container_width=True)
