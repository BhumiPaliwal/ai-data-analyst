import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from google import genai

# 1. Broad Page Configurations
st.set_page_config(page_title="Advanced Data Science Workspace", layout="wide")

# STEP 5: Premium Minimalist UX Styling Overrides
st.markdown("""
<style>
    /* Premium card background styling */
    .stElementContainer div[data-testid="stVerticalBlock"] > div {
        font-family: 'Inter', sans-serif;
    }
    h1 { color: #0f172a; text-align: center; font-size: 40px; font-weight: 800; letter-spacing: -1px; margin-bottom: 5px; }
    h2, h3 { color: #1e40af; font-weight: 700; }
    
    /* Smooth rounded corners and soft shadows for tables and modules */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.05);
    }
    
    /* Clean button typography */
    .stButton > button { background-color: #2563eb; color: white; border-radius: 8px; font-weight: 600; width: 100%; border: none; }
    .stButton > button:hover { background-color: #1d4ed8; color: white; }
    .stDownloadButton > button { background-color: #059669; color: white; border-radius: 8px; font-weight: 600; width: 100%; border: none; }
    .stDownloadButton > button:hover { background-color: #047857; color: white; }
    
    /* Modern tab styling */
    .stTabs [data-baseweb="tab"] { font-weight: 600; font-size: 15px; color: #475569; }
    .stTabs [data-baseweb="tab"]:hover { color: #2563eb; }
</style>
""", unsafe_allow_html=True)

st.title("🔬 Advanced Data Science Workspace")
st.markdown("<div style='text-align: center; color: #64748b; font-size: 16px; margin-bottom: 30px;'>Enterprise-grade sandbox featuring real-time data inspection, custom statistical metrics, and conversational deep AI context engines.</div>", unsafe_allow_html=True)

# STEP 4: Elegant Sidebar Accordion Grouping
st.sidebar.title("🛠️ Enterprise Control Center")

with st.sidebar.expander("🔑 AI Credentials & Gateway", expanded=False):

    gemini_api_key = st.text_input("Gemini Engine Key", type="password")

# Handle API keys gracefully without crashing if secrets file doesn't exist
try:
    final_api_key = st.secrets.get("GEMINI_API_KEY", gemini_api_key)
except Exception:
    final_api_key = gemini_api_key


with st.sidebar.expander("📁 Data Pipeline Ingestion", expanded=True):

    uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

# 3. Smart Dataset File History Manager
if "datasets" not in st.session_state:
    st.session_state.datasets = {}

if uploaded_file is not None:
    file_name = uploaded_file.name
    if file_name not in st.session_state.datasets:
        st.session_state.datasets[file_name] = pd.read_csv(uploaded_file)
    
    selected_file = st.sidebar.selectbox("Active Workspace File", list(st.session_state.datasets.keys()), index=list(st.session_state.datasets.keys()).index(file_name))
    df = st.session_state.datasets[selected_file]

    rows, columns = df.shape
    total_missing = df.isnull().sum().sum()
    
    # STEP 2: Containerized Corporate Dashboard KPI Cards
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

    # TAB 2: PLOTLY VISUALIZER (Including advanced aggregation)
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
            
            # Histogram math adjustment controls
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

    # TAB 3: ANOMALY ISOLATION (Using Step 3 Status Indicators)
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
                
                # STEP 3: Corporate Interactive Status System
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
        with st.container(border=True):
            st.subheader("💬 Continuous Context Conversations")
            if "chat_history" not in st.session_state: st.session_state.chat_history = []
            
            if st.button("Purge Chat Logs Memory"):
                st.session_state.chat_history = []
                st.rerun()

            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]): st.markdown(msg["content"])

            if ai_question := st.chat_input("Ask macro insight projections..."):
                st.session_state.chat_history.append({"role": "user", "content": ai_question})
                with st.chat_message("user"): st.markdown(ai_question)

                active_key = final_api_key if final_api_key else gemini_api_key

                if not active_key:
                    st.error("Missing Gemini Key in authentication dashboard panels.")
                else:
                    try:
                        client = genai.Client(api_key=active_key)
                        dataset_summary = f"Columns: {list(df.columns)} | Shape: {df.shape}\nStats Snapshot:\n{df.describe().to_string()}"
                        
                        history_context = ""
                        for chat in st.session_state.chat_history[-6:]:
                            history_context += f"{chat['role'].upper()}: {chat['content']}\n"

                        full_prompt = f"Context metrics profile:\n{dataset_summary}\n\nThread Stream:\n{history_context}\nASSISTANT:"
                        
                        response = client.models.generate_content(model="gemini-2.5-flash", contents=full_prompt)
                        with st.chat_message("assistant"): st.markdown(response.text)
                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Internal API Execution Fault: {e}")

    # TAB 5: DATA TRANSFORMER
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
                
        with st.container(border=True):
            st.subheader("Export Cleaned Data Structure")
            st.download_button(label="Export Pipeline CSV Output File", data=df.to_csv(index=False), file_name="transformed_dataset.csv", mime="text/csv")
else:
    st.info("Drop file sets inside workspace configuration sidebars to unpack computing structures.")