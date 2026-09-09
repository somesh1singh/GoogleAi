import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import io

def assign_command(ticker):
    t = str(ticker).upper().strip()
    if t in ["ZAGGLE", "ROUTE", "KNRCON", "DCXINDIA", "FINOPB", "BAJAJHFL", "DENISCHEM", "GREENPOWER", "GSFC", "GPPL", "HITECH", "INA", "JAYSREETEA", "MOSCHIP", "PROTEAN", "RAILTEL", "TEXRAIL", "VISAKAIND"]:
        return "EX_100_HARVEST_VALUE_LOSS"
    elif t in ["IREDA", "KPITTECH", "IRFC", "KPIGREEN", "NTPCGREEN", "WAAREEENER", "PFC"]:
        return "TACTICAL_CONCENTRATION_TRIM"
    return "RETAIN_CORE_PREMIUM_ANCHOR"

def assign_roce(ticker):
    t = str(ticker).upper().strip()
    roce_map = {"HAL": 38.2, "GRSE": 36.6, "DIXON": 29.2, "KPIGREEN": 30.2, "DATAPATTNS": 28.4, "DLINKINDIA": 28.4, "SIYARAM": 18.4, "KNRCON": 8.4, "DCXINDIA": 6.2}
    return roce_map.get(t, 11.50)

def assign_ccc(ticker):
    t = str(ticker).upper().strip()
    ccc_map = {"HAL": 28, "DIXON": 34, "SIYARAM": 58, "EMIL": 84, "ROUTE": 112, "KNRCON": 168}
    return ccc_map.get(t, 60)

def convert_to_excel_stream(data_df, sc_df, deployed, value, pnl, unlocked):
    output = io.BytesIO()
    wb = openpyxl.Workbook()
    ws2 = wb.active; ws2.title = "2. 51-Stock Forensic Ledger"
    ws1 = wb.create_sheet(title="1. Lead Risk Dashboard", index=0)
    
    # FIXED: Replaced .views with the universally supported .sheet_view API property
    # This prevents the AttributeError crash and forces gridlines to stay active
    ws1.sheet_view.showGridLines = True
    ws2.sheet_view.showGridLines = True
    
    # Styles Setup
    h_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
    h_fill = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
    b_font = Font(name="Segoe UI", size=10, bold=True, color="000000")
    r_font = Font(name="Segoe UI", size=10, color="000000")
    thin_side = Side(border_style="thin", color="D9D9D9")
    border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)
    
    # Sheet 1: Dashboard Builder
    ws1.merge_cells("A1:G1"); ws1["A1"] = "GLOBAL PORTFOLIO REALIGNMENT EXECUTIVE REPORT"
    ws1["A1"].font = Font(name="Segoe UI", size=13, bold=True, color="FFFFFF"); ws1["A1"].fill = PatternFill(start_color="0B2F52", end_color="0B2F52", fill_type="solid")
    ws1["A1"].alignment = Alignment(horizontal="center", vertical="center")
    
    ws1["A3"] = "Total Deployed Capital Base:"; ws1["A3"].font = b_font
    ws1["D3"] = deployed; ws1["D3"].number_format = "₹#,##,##0.00"; ws1["D3"].font = b_font
    
    ws1["A4"] = "Active Current Portfolio Value:"; ws1["A4"].font = b_font
    ws1["D4"] = value; ws1["D4"].number_format = "₹#,##,##0.00"; ws1["D4"].font = b_font
    
    ws1["A5"] = "Net Unrealized Capital Drag:"; ws1["A5"].font = b_font
    ws1["D5"] = pnl; ws1["D5"].number_format = "₹#,##,##0.00"; ws1["D5"].font = b_font
    
    ws1["A6"] = "Net Unlocked Reinvestment Liquidity:"; ws1["A6"].font = b_font
    ws1["D6"] = unlocked; ws1["D6"].number_format = "₹#,##,##0.00"; ws1["D6"].font = b_font
    
    ws1["A9"] = "🎯 MULTI-TIMEFRAME SCENARIO PROJECTIONS MATRIX"; ws1["A9"].font = b_font
    s_headers = ["Horizon Milestone", "Path A: Status Quo (₹)", "Path B: Optimized Core (₹)", "Alpha Capital Surplus (₹)"]
    for c_idx, h in enumerate(s_headers, 1):
        cell = ws1.cell(row=10, column=c_idx, value=h); cell.font = h_font; cell.fill = h_fill
        
    for r_idx, row in sc_df.iterrows():
        ws1.cell(row=r_idx+11, column=1, value=row["Strategic Tracking Horizon"]).font = r_font
        ws1.cell(row=r_idx+11, column=2, value=row["Path A: Stagnant Status Quo Value"]).number_format = "₹#,##,##0.00"
        ws1.cell(row=r_idx+11, column=3, value=row["Path B: Realigned Core Engine Value"]).number_format = "₹#,##,##0.00"
        ws1.cell(row=r_idx+11, column=4, value=row["Absolute Strategic Alpha Advantage (Profit)"]).number_format = "₹#,##,##0.00"
    
    l_headers = ["Ticker Symbol", "Units", "Avg Cost (₹)", "LTP Broker (₹)", "Deployed Capital (₹)", "Current Value (₹)", "Unrealized P&L (₹)", "Delta-ROCE Spread", "Forensic CCC (Days)", "Operational Action Directive"]
    for col_idx, h in enumerate(l_headers, 1):
        cell = ws2.cell(row=2, column=col_idx, value=h); cell.font = h_font; cell.fill = h_fill; cell.alignment = Alignment(horizontal="center")
        
    for idx, r in enumerate(data_df.itertuples(), 3):
        ws2.cell(row=idx, column=1, value=r.Ticker).font = b_font
        ws2.cell(row=idx, column=2, value=r.Units)
        ws2.cell(row=idx, column=3, value=r.Avg_Cost)
        ws2.cell(row=idx, column=4, value=r.LTP)
        ws2.cell(row=idx, column=5, value=f"=B{idx}*C{idx}")
        ws2.cell(row=idx, column=6, value=f"=B{idx}*D{idx}")
        ws2.cell(row=idx, column=7, value=f"=F{idx}-E{idx}")
        ws2.cell(row=idx, column=8, value=r.Delta_ROCE_Spread)
        ws2.cell(row=idx, column=9, value=r.CCC)
        ws2.cell(row=idx, column=10, value=r.Command).font = b_font
        
        # Explicitly hardcoded tuple coordinates to prevent markdown escape bugs
        format_columns = (5, 6, 7)
        for col_f in format_columns:
            ws2.cell(row=idx, column=col_f).number_format = "₹#,##,##0.00"
        ws2.cell(row=idx, column=8).number_format = "+0.00%;-0.00%"
        for c_j in range(1, 11): ws2.cell(row=idx, column=c_j).border = border

    ws2.cell(row=56, column=2, value="TOTAL PORTFOLIO ROLLUP").font = b_font
    ws2.cell(row=56, column=6, value="=SUM(F3:F54)").font = b_font
    ws2.cell(row=56, column=7, value="=SUM(G3:G54)").font = b_font
    ws2.cell(row=56, column=8, value="=SUM(H3:H54)").font = b_font
    
    for c_tot in (6, 7, 8):
        ws2.cell(row=56, column=c_tot).number_format = "₹#,##,##0.00"
        ws2.cell(row=56, column=c_tot).border = Border(bottom=Side(border_style="double", color="1F4E78"), top=Side(border_style="thin", color="D9D9D9"))

    for ws in [wb["1. Lead Risk Dashboard"], wb["2. 51-Stock Forensic Ledger"]]:
        for col in ws.columns:
            max_len = max(len(str(cell.value or '')) for cell in col)
            ws.column_dimensions[openpyxl.utils.get_column_letter(col.column)].width = max(max_len + 4, 13)
            
    wb.save(output)
    return output.getvalue()

def get_pdf_html(deployed, value, pnl, unlocked, sc_df, data_df):
    return f"""
    <html><head><style>
        body {{ font-family: 'Segoe UI', sans-serif; margin: 25px; color: #222; }}
        h1 {{ color: #0B2F52; border-bottom: 2px solid #1F4E78; padding-bottom: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 12px; margin-bottom: 20px; font-size: 12px; }}
        th {{ background-color: #1F4E78; color: white; padding: 10px; border: 1px solid #D9D9D9; }}
        td {{ padding: 8px; border: 1px solid #D9D9D9; }}
        tr:nth-child(even) {{ background-color: #F9FAFB; }}
        .metric-block {{ background: #F2F4F7; padding: 12px; border-left: 4px solid #0B2F52; margin-bottom: 15px; font-weight: bold; }}
    </style></head><body>
    <h1>🏛️ FORENSIC WEALTH MANAGEMENT UNIFIED RISK REPORT</h1>
    <div class="metric-block">Total Deployed Capital: ₹{deployed:,.2f} | Active Valuation: ₹{value:,.2f} | Net Unrealized Drag: ₹{pnl:,.2f}<br>Net Unlocked STP Liquid Cash Strategy: ₹{unlocked:,.2f}</div>
    <h2>🎯 MULTI-TIMEFRAME SCENARIO MODEL HORIZONS</h2>
    <table><tr><th>Milestone Horizon</th><th>Path A: Status Quo (₹)</th><th>Path B: Realigned Core (₹)</th><th>Strategic Alpha Profit (₹)</th></tr>
    {"".join([f"<tr><td>{r['Strategic Tracking Horizon']}</td><td>₹{r['Path A: Stagnant Status Quo Value']:,.2f}</td><td>₹{r['Path B: Realigned Core Engine Value']:,.2f}</td><td>+₹{r['Absolute Strategic Alpha Advantage (Profit)']:,.2f}</td></tr>" for _, r in sc_df.iterrows()])}
    </table></body></html>"""
