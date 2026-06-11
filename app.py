import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import os
from streamlit_drawable_canvas import st_canvas

# 1. Broad Page Configurations
st.set_page_config(page_title="Advanced Data Science Workspace", layout="wide")

# Premium Corporate UX & Client-Ready Styling Overrides
st.markdown("""
<style>
    /* Global Font & Canvas Adjustments */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {
        font-family: 'Inter', sans-serif;
        background-color: #f8fafc; /* Clean off-white corporate canvas */
    }
    
    /* Executive Headers */
    h1 { 
        color: #0f172a; 
        text-align: center; 
        font-size: 38px; 
        font-weight: 800; 
        letter-spacing: -1px; 
        margin-bottom: 2px; 
    }
    h2, h3, [data-testid="stMarkdownContainer"] h3 { 
        color: #1e3a8a; /* Deep Corporate Navy */
        font-weight: 700; 
        letter-spacing: -0.5px;
    }
    
    /* Clean Main Canvas Container Cards */
    div[data-testid="stContainer"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 12px !important;
        padding: 24px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03), 0 2px 4px -2px rgba(0, 0, 0, 0.03) !important;
        margin-bottom: 20px;
    }
    
    /* Data Grid Framework */
    .stDataFrame {
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        overflow: hidden;
    }
    
    /* --- PREMIUM GRADIENT SIDEBAR --- */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f172a 0%, #1e3a8a 100%) !important; /* Elegant Navy to Midnight Gradient */
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    
    /* --- HIGH-CONTRAST SOLID WHITE EXPANDER BOXES --- */
    [data-testid="stSidebar"] div[data-testid="stExpander"] {
        background-color: #ffffff !important; /* Force boxes to stay clean solid white */
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1) !important;
        margin-bottom: 15px;
    }
    
    /* Expander Headers Text styling (Dark text for white boxes) */
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary p,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary span,
    [data-testid="stSidebar"] div[data-testid="stExpander"] summary div {
        color: #0f172a !important; /* Clear dark grey/black heading text */
        font-weight: 600 !important;
        font-size: 14px !important;
    }
    [data-testid="stSidebar"] div[data-testid="stExpander"] svg {
        fill: #0f172a !important; /* Dark drop-down arrow icon */
    }

    /* Internal Text Labels styling inside the white boxes */
    [data-testid="stSidebar"] div[data-testid="stExpander"] label, 
    [data-testid="stSidebar"] div[data-testid="stExpander"] p, 
    [data-testid="stSidebar"] div[data-testid="stExpander"] small,
    [data-testid="stSidebar"] div[data-testid="stExpander"] [data-testid="stMarkdownContainer"] p {
        color: #334155 !important; /* Sharp, legible dark grey description labels */
        font-weight: 500 !important;
    }
    
    /* Input field styling adjustments inside white box panels */
    [data-testid="stSidebar"] div[data-testid="stExpander"] input {
        background-color: #f8fafc !important; 
        color: #0f172a !important;
        border: 1px solid #cbd5e1 !important;
    }
    
    /* High-Performance Action Buttons (Corporate Navy) */
    .stButton > button { 
        background-color: #2563eb; 
        color: white; 
        border-radius: 8px; 
        font-weight: 600; 
        width: 100%; 
        border: none;
        padding: 10px 24px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
    }
    .stButton > button:hover { 
        background-color: #1d4ed8; 
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(29, 78, 216, 0.3);
    }
    
    /* Target Success Buttons (Data / Pipeline Export Green) */
    .stDownloadButton > button { 
        background-color: #059669; 
        color: white; 
        border-radius: 8px; 
        font-weight: 600; 
        width: 100%; 
        border: none;
        padding: 10px 24px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 4px rgba(5, 150, 105, 0.2);
    }
    .stDownloadButton > button:hover { 
        background-color: #047857; 
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(4, 120, 87, 0.3);
    }
    
    /* Modern Dashboard Navigation Tab Layout */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #f1f5f9;
        padding: 6px;
        border-radius: 10px;
        border: 1px solid #e2e8f0;
    }
    .stTabs [data-baseweb="tab"] { 
        font-weight: 600; 
        font-size: 14px; 
        color: #64748b; 
        background-color: transparent;
        padding: 8px 16px;
        border-radius: 6px;
        transition: all 0.15s ease;
    }
    .stTabs [data-baseweb="tab"]:hover { 
        color: #0f172a; 
        background-color: rgba(255, 255, 255, 0.6);
    }
    .stTabs [aria-selected="true"] {
        color: #2563eb !important;
        background-color: #ffffff !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Advanced Data Science Workspace")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 15px; margin-bottom: 35px; font-weight: 400;'>Enterprise-grade sandbox featuring real-time data inspection, custom statistical metrics, and conversational deep AI context engines.</div>", unsafe_allow_html=True)

# Elegant Sidebar Accordion Grouping
st.sidebar.title("🛠️ Enterprise Control Center")

# File Ingestion UI
with st.sidebar.expander("📁 Data Pipeline Ingestion", expanded=True):
    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

# 3. Smart Dataset File History Manager
if "datasets" not in st.session_state:
    st.session_state.datasets = {}

if uploaded_file is not None:
    file_name = uploaded_file.name
    if file_name not in st.session_state.datasets:
        st.session_state.datasets[file_name] = pd.read_csv(uploaded_file, encoding='latin-1')
    
    file_list = list(st.session_state.datasets.keys())
    if "selected_file_key" not in st.session_state or st.session_state.selected_file_key not in file_list:
        st.session_state.selected_file_key = file_name
        
    selected_file = st.sidebar.selectbox(
        "Active Workspace File", 
        file_list, 
        index=file_list.index(st.session_state.selected_file_key),
        key="file_selector_dropdown"
    )
    st.session_state.selected_file_key = selected_file
    
    df = st.session_state.datasets[selected_file]

    rows, columns = df.shape
    total_missing = df.isnull().sum().sum()
    
    # Containerized Corporate Dashboard KPI Cards
    with st.container(border=True):
        st.markdown("### 📊 Global Workspace Pulse")
        col1, col2, col3 = st.columns(3)
        col1.metric(label="Total Log Entries (Rows)", value=f"{rows:,}", delta="Data Stack Active")
        col2.metric(label="Features Mapped (Columns)", value=columns)
        
        # Calculate overall data health score percentage
        total_cells = rows * columns
        health_rate = ((total_cells - total_missing) / total_cells) * 100 if total_cells > 0 else 100
        col3.metric(label="Data Integrity Rate", value=f"{health_rate:.1f}%", delta=f"{total_missing} missing elements", delta_color="inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # Core Tab Framework Navigation
    tabs = st.tabs(["📋 Profile Explorer", "📈 Plotly Visualizer", "🚨 Anomaly Isolation", "💬 Deep Brain AI", "🧹 Data Transformer"])
    
    # TAB 1: PROFILE EXPLORER
    with tabs[0]:
        with st.container(border=True):
            st.subheader("Interactive Cell Matrix Workspace")
            edited_dataframe = st.data_editor(df.head(20), key=f"editor_{selected_file}")
            if st.button("Commit Cell Modifications"):
                st.session_state.datasets[selected_file].update(edited_dataframe)
                st.success("Target data frame matrix cells synchronized!")
            
        with st.container(border=True):
            st.subheader("Statistical Field Dispersions")
            st.dataframe(df.describe(include='all').fillna(''))

    # TAB 2: PLOTLY VISUALIZER
    with tabs[1]:
        with st.container(border=True):
            st.subheader("Real-Time Analytics Render Engine")
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            all_cols = df.columns.tolist()
            
            v_col1, v_col2, v_col3 = st.columns(3)
            with v_col1: chart_type = st.selectbox("Engine Layout style", ["Scatter Plot", "Box Plot", "Histogram", "Line Chart"])
            with v_col2: x_axis = st.selectbox("X Dimension Axis", all_cols)
            with v_col3: y_axis = st.selectbox("Y Dimension Axis (Numeric)", numeric_cols if numeric_cols else all_cols)
            
            color_by = st.selectbox("Color Segments By (Categorical)", [None] + df.select_dtypes(include=['object']).columns.tolist())
            
            # Histogram customization
            st.markdown("<small>📊 **Histogram Parameter Customization** (Only applies when 'Histogram' is selected)</small>", unsafe_allow_html=True)
            h_col1, h_col2 = st.columns(2)
            with h_col1: hist_func = st.selectbox("Vertical Axis Calculation", ["count", "sum", "avg", "min", "max"])
            with h_col2: hist_target = st.selectbox("Value Column to Calculate", numeric_cols if numeric_cols else all_cols)
            
            try:
                if chart_type == "Scatter Plot":
                    fig = px.scatter(df, x=x_axis, y=y_axis, color=color_by, template="plotly_white")
                elif chart_type == "Box Plot":
                    fig = px.box(df, x=x_axis, y=y_axis, color=color_by, template="plotly_white")
                elif chart_type == "Histogram":
                    fig = px.histogram(
                        df, 
                        x=x_axis, 
                        y=hist_target if hist_func != "count" else None, 
                        histfunc=hist_func, 
                        color=color_by, 
                        template="plotly_white"
                    )
                elif chart_type == "Line Chart":
                    fig = px.line(df, x=x_axis, y=y_axis, color=color_by, template="plotly_white")
                    
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Could not build visualization parameters: {e}")

    # TAB 3: ANOMALY ISOLATION
    with tabs[2]:
        with st.container(border=True):
            st.subheader("Statistical Outlier Anomaly Detection")
            st.markdown("Isolate anomalies using the mathematical Interquartile Range standard: $IQR = Q_3 - Q_1$. Values beyond $1.5 \\times IQR$ are isolated.")
            
            if numeric_cols:
                target_anomaly_col = st.selectbox("Target Column for Structural Audit", numeric_cols)
                
                q1 = df[target_anomaly_col].quantile(0.25)
                q3 = df[target_anomaly_col].quantile(0.75)
                iqr = q3 - q1
                lower_bound = q1 - 1.5 * iqr
                upper_bound = q3 + 1.5 * iqr
                
                anomalies_df = df[(df[target_anomaly_col] < lower_bound) | (df[target_anomaly_col] > upper_bound)]
                
                with st.status("Running Structural Data Audit...", expanded=True) as status:
                    st.write("Extracting localized array quantiles...")
                    st.write(f"Upper Statistical Boundary set at: `{upper_bound:.2f}`")
                    st.write(f"Lower Statistical Boundary set at: `{lower_bound:.2f}`")
                    
                    if not anomalies_df.empty:
                        status.update(label=f"Audit Completed: {len(anomalies_df)} Clear Outliers Tracked!", state="error")
                        st.dataframe(anomalies_df)
                    else:
                        status.update(label="Audit Completed: No anomalous rows tracked.", state="complete")
            else:
                st.info("No numeric tracking points available for anomaly checking.")

    # TAB 4: DEEP BRAIN AI CHAT
    with tabs[3]:
        st.subheader("💬 Dynamic Local Data Analyst AI")
        st.markdown("<small>⚡ *Generates real-time Python analytics code locally using Phi-3 with Auto-Guardrails.*</small>", unsafe_allow_html=True)
        
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []
            
        if st.button("Purge Chat Logs Memory"):
            st.session_state.chat_history = []
            st.rerun()
            
        for msg in st.session_state.chat_history:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                
        ai_question = st.chat_input("Ask any data insight (e.g., 'What are the top 2 insights of this dataset?')...")
        
        if ai_question:
            with st.chat_message("user"):
                st.markdown(ai_question)
            st.session_state.chat_history.append({"role": "user", "content": ai_question})
            
            with st.chat_message("assistant"):
                try:
                    import ollama
                    response_placeholder = st.empty()
                    
                    columns_info = ", ".join(df.columns.tolist())
                    data_types = ", ".join([f"{col} ({dtype})" for col, dtype in zip(df.columns, df.dtypes)])
                    
                    system_instruction = (
                        "You are a strict Python data analysis backend assistant. Based on the dataset columns provided, "
                        "write EXACTLY ONE executable statement of pandas code that returns the answer to the user's question. "
                        "The dataframe variable is named 'df'. "
                        "CRITICAL: Do not include markdown formatting, backticks, comments, or any conversational text. "
                        "Return ONLY the plain python string. Example: df.groupby('Region')['Sales'].sum().nlargest(2)"
                    )
                    
                    full_prompt = f"{system_instruction}\n\nColumns available: {columns_info}\nData Types: {data_types}\n\nUser Question: {ai_question}"
                    
                    with st.spinner("Generating Live Analytical Query..."):
                        res = ollama.generate(model='phi3', prompt=full_prompt)
                        generated_code = res['response'].strip()
                        
                        if "```python" in generated_code:
                            generated_code = generated_code.split("```python")[1].split("```")[0].strip()
                        elif "```" in generated_code:
                            generated_code = generated_code.split("```")[1].strip()
                            
                        lines = [line.strip() for line in generated_code.split('\n') if line.strip() and not line.strip().startswith(('#', 'Explain', 'Here'))]
                        if lines:
                            generated_code = lines[0]

                    try:
                        result_output = eval(generated_code)
                        format_prompt = f"Convert this calculation result into a polite, professional, short sentence for a client dashboard: Question: {ai_question} -> Result Data: {result_output}"
                        
                        full_response = ""
                        stream = ollama.generate(model='phi3', prompt=format_prompt, stream=True)
                        for chunk in stream:
                            full_response += chunk['response']
                            response_placeholder.markdown(full_response + "▌")
                            
                        response_placeholder.markdown(full_response)
                        st.session_state.chat_history.append({"role": "assistant", "content": full_response})
                        
                    except Exception as code_err:
                        fallback_prompt = f"Answer this question based on general knowledge of a global superstore dataset: {ai_question}"
                        res = ollama.generate(model='phi3', prompt=fallback_prompt)
                        response_placeholder.markdown(res['response'])
                        st.session_state.chat_history.append({"role": "assistant", "content": res['response']})
                        
                except Exception as e:
                    st.error(f"Local Model Connection Error: {e}")

    # TAB 5: DATA TRANSFORMER & REPORT ENGINE
    with tabs[4]:
        with st.container(border=True):
            st.subheader("Advanced Data Wrangling Options")
            
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Drop Duplicate Data Rows"):
                    st.session_state.datasets[selected_file] = df.drop_duplicates()
                    st.success("Data rows purged of overlaps!")
                    st.rerun()
            with c2:
                if st.button("Impute Null Numeric Values to Column Means"):
                    for col in numeric_cols:
                        st.session_state.datasets[selected_file][col] = df[col].fillna(df[col].mean())
                    st.success("Numeric fields updated with column averages.")
                    st.rerun()
                
        # Main Report Engine Interface Box
        with st.container(border=True):
            st.subheader("📊 Executive Summary Report Generator")
            st.markdown("<small>📄 *Generates a branded, presentation-ready PDF report summarizing active workspace telemetry metrics.*</small>", unsafe_allow_html=True)
            
            # 1. Commentary Box Input Frame
            exec_notes = st.text_area("Add Custom Executive Commentary/Notes (Optional):", placeholder="Type any observations or notes to include in the official PDF attachment...")
            
            # 2. Bounded Live Signature Whiteboard Widget Block
            st.markdown("### ✍️ Executive Authorization Signature")
            st.markdown("<small>🖊️ *Draw your digital authorization inside the box below before compiling.*</small>", unsafe_allow_html=True)
            
            # Clean CSS rule integration
            st.markdown(
                """
                <style>
                iframe[title="streamlit_drawable_canvas.st_canvas"] {
                    border: 2px dashed #cbd5e1 !important;
                    border-radius: 8px !important;
                    background-color: #f8fafc !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )
            
            # Cleaned Python Indentation (Zero hidden web-text characters)
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)", 
                stroke_width=3,                      
                stroke_color="#0f172a",              
                background_color="#f8fafc",          
                height=150,                          
                width=500,                           
                drawing_mode="freedraw",
                key="executive_signature_pad",
            )

            # 3. Compile Core Action Button Pipeline Trigger
            if st.button("Compile Executive PDF Report"):
                from fpdf import FPDF
                import io
                
                try:
                    class CorporatePDF(FPDF):
                        def header(self):
                            self.set_fill_color(15, 23, 42)
                            self.rect(0, 0, 210, 6, "F")
                            
                        def footer(self):
                            self.set_y(-15)
                            self.set_font("Helvetica", "I", 8)
                            self.set_text_color(148, 163, 184)
                            self.cell(0, 10, f"Page {self.page_no()} | Confidential Enterprise Workspace Asset", border=0, ln=False, align="L")
                            self.cell(0, 10, "System Data Science Core Engine v2.0", border=0, ln=False, align="R")

                    pdf = CorporatePDF()
                    pdf.set_auto_page_break(auto=True, margin=20)
                    pdf.add_page()
                    
                    pdf.ln(6)
                    pdf.set_font("Helvetica", "B", 20)
                    pdf.set_text_color(30, 58, 138)
                    pdf.cell(190, 10, "EXECUTIVE WORKSPACE TELEMETRY REPORT", ln=True, align="L")
                    
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(100, 116, 139)
                    pdf.cell(190, 5, txt=f"Generated System Analytics Log - Active File: {selected_file}", ln=True, align="L")
                    
                    pdf.ln(2)
                    pdf.set_draw_color(37, 99, 235)
                    pdf.set_line_width(0.8)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(6)
                    
                    pdf.set_font("Helvetica", "B", 13)
                    pdf.set_text_color(30, 58, 138)
                    pdf.cell(190, 8, "1. Executive Position Summary", ln=True)
                    
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(51, 65, 85)
                    summary_text = (
                        f"This document formalizes the internal diagnostic evaluation of the target asset data structure ({selected_file}). "
                        f"The operational ecosystem parsed a raw array space totaling {rows:,} matrix entries across {columns} mapped analytical fields. "
                        f"System validation processes confirmed a core structural runtime operational integrity rating of {health_rate:.2f}%."
                    )
                    pdf.multi_cell(190, 5, txt=summary_text)
                    pdf.ln(6)
                    
                    pdf.set_font("Helvetica", "B", 13)
                    pdf.set_text_color(30, 58, 138)
                    pdf.cell(190, 8, "2. Operational Performance & System Telemetry", ln=True)
                    pdf.ln(2)
                    
                    pdf.set_font("Helvetica", "B", 10)
                    pdf.set_fill_color(241, 245, 249)
                    pdf.set_text_color(15, 23, 42)
                    pdf.cell(110, 8, "  Evaluated Telemetry Vector Column", border=1, align="L", fill=True)
                    pdf.cell(80, 8, "Extracted System Metric Value  ", border=1, align="C", fill=True)
                    pdf.ln()
                    
                    pdf.set_font("Helvetica", "", 10)
                    metrics_data = [
                        ("Total Data Records Ingested (DataFrame Rows)", f"{rows:,} entries"),
                        ("Mapped Dimensional Constraints (DataFrame Columns)", f"{columns} dimensions"),
                        ("Target Structural Integrity Index Ratio", f"{health_rate:.1f}% status code"),
                        ("Discovered Null / Blank Elements inside Matrix", f"{total_missing} elements"),
                        ("Numerical Columns Registered in active memory", f"{len(numeric_cols)} features")
                    ]
                    
                    for label, val in metrics_data:
                        pdf.cell(110, 7, f"  {label}", border=1, align="L")
                        pdf.cell(80, 7, val, border=1, align="C")
                        pdf.ln()
                        
                    pdf.ln(6)
                    
                    pdf.set_font("Helvetica", "B", 13)
                    pdf.set_text_color(30, 58, 138)
                    pdf.cell(190, 8, "3. Localized Brain AI Chat Interface Summary Log", ln=True)
                    pdf.ln(2)
                    
                    if st.session_state.chat_history:
                        for msg in st.session_state.chat_history[-4:]:
                            role_label = "User Prompt" if msg["role"] == "user" else "AI Analytical Insight"
                            
                            clean_text = (msg["content"]
                                          .replace("•", "-")
                                          .replace("—", "-")
                                          .replace("`", "'")
                                          .replace("“", '"')
                                          .replace("”", '"'))
                            clean_text = clean_text.encode('latin-1', 'ignore').decode('latin-1')
                            
                            pdf.set_font("Helvetica", "B", 9)
                            if msg["role"] == "user":
                                pdf.set_text_color(37, 99, 235)
                            else:
                                pdf.set_text_color(5, 150, 105)
                                
                            pdf.cell(190, 5, txt=f"[{role_label}]", ln=True)
                            
                            pdf.set_font("Helvetica", "", 10)
                            pdf.set_text_color(51, 65, 85)
                            pdf.multi_cell(190, 5, txt=clean_text)
                            pdf.ln(2)
                    else:
                        pdf.set_font("Helvetica", "I", 10)
                        pdf.set_text_color(100, 116, 139)
                        pdf.cell(190, 6, txt="No conversational interactive logic executed during this processing timeframe.", ln=True)
                    
                    pdf.ln(6)
                    
                    if exec_notes:
                        pdf.set_font("Helvetica", "B", 13)
                        pdf.set_text_color(30, 58, 138)
                        pdf.cell(190, 8, "4. Strategic Notes & Custom Advisory Commentary", ln=True)
                        pdf.ln(2)
                        
                        pdf.set_font("Helvetica", "", 10)
                        pdf.set_text_color(15, 23, 42)
                        clean_notes = exec_notes.encode('latin-1', 'ignore').decode('latin-1')
                        pdf.multi_cell(190, 5, txt=clean_notes)
                        pdf.ln(6)
                        
                    pdf.ln(4)
                    pdf.set_draw_color(203, 213, 225)
                    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
                    pdf.ln(4)
                    
                    pdf.set_font("Helvetica", "B", 11)
                    pdf.set_text_color(30, 58, 138)
                    pdf.cell(190, 6, txt="5. Strategic Sign-Off Verification Matrix", ln=True)
                    pdf.ln(12)
                    
                    current_y = pdf.get_y()
                    pdf.set_font("Helvetica", "", 9)
                    pdf.set_text_color(100, 116, 139)
                    
                    pdf.line(15, current_y, 85, current_y)
                    
                    if canvas_result is not None and canvas_result.image_data is not None:
                        from PIL import Image
                        sig_image = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
                        sig_buffer = io.BytesIO()
                        sig_image.save(sig_buffer, format="PNG")
                        sig_buffer.seek(0)
                        pdf.image(sig_buffer, x=22, y=current_y - 14, w=55, h=13)
                    
                    pdf.set_xy(15, current_y + 2)
                    pdf.cell(70, 4, txt="Reporting Systems Officer Signature", ln=True, align="C")
                    pdf.set_x(15)
                    pdf.cell(70, 4, txt="Bhumi Paliwal", ln=True, align="C")
                    
                    pdf.line(125, current_y, 195, current_y)
                    pdf.set_xy(125, current_y + 2)
                    pdf.cell(70, 4, txt="Executive Corporate Reviewer Sign-off", ln=True, align="C")
                    pdf.set_x(125)
                    pdf.cell(70, 4, txt="Date: ____ / ____ / 2026", ln=True, align="C")

                    pdf_buffer = io.BytesIO()
                    pdf.output(pdf_buffer)
                    pdf_buffer.seek(0)
                    
                    st.success("Advanced Executive Presentation Portfolio Brief Compiled Successfully!")
                    st.download_button(
                        label="📥 Download Official Extended Executive PDF Report",
                        data=pdf_buffer,
                        file_name=f"Comprehensive_Executive_Brief_{selected_file.split('.')[0]}.pdf",
                        mime="application/pdf"
                    )
                    
                except Exception as pdf_error:
                    st.error(f"Error compiling deep document profile matrices: {pdf_error}")    

        # Core CSV export channel container
        with st.container(border=True):
            st.subheader("Export Cleaned Data Structure")
            st.download_button(label="Export Pipeline CSV Output File", data=df.to_csv(index=False), file_name="transformed_dataset.csv", mime="text/csv")
# --- PERSISTENT FOOTER SIGNATURE ---
st.markdown(
    """
    <style>
    .fixed-footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: transparent;
        color: #64748b; 
        text-align: right;
        padding-right: 30px;
        padding-bottom: 12px;
        font-size: 13px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        letter-spacing: 0.3px;
        z-index: 999999;
        pointer-events: none;
    }
    </style>
    <div class="fixed-footer">
        Developed by Bhumi Paliwal
    </div>
    """,
    unsafe_allow_html=True
)