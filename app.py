import streamlit as st
import pandas as pd
from google import genai

st.set_page_config(page_title="AI Data Analyst Agent", layout="wide")

st.markdown("""
<style>
    .main { background-color: #f7f9fc; }

    h1 {
        color: #1f2937;
        text-align: center;
        font-size: 42px;
    }

    h2, h3 { color: #2563eb; }

    .stButton > button {
        background-color: #2563eb;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
    }

    .stDownloadButton > button {
        background-color: #16a34a;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 18px;
        font-weight: 600;
    }

    [data-testid="stMetricValue"] {
        color: #2563eb;
        font-weight: 700;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

st.title("AI Data Analyst Agent")

st.markdown("""
<div style='text-align: center; font-size: 18px; color: #4b5563; margin-bottom: 25px;'>
Upload a CSV dataset, explore it, clean it, visualize it, and generate useful insights.
</div>
""", unsafe_allow_html=True)

st.sidebar.title("Project Menu")
st.sidebar.write("AI Data Analyst Agent")
st.sidebar.write("Built with Python, Streamlit, and Pandas")

st.sidebar.subheader("Features")
st.sidebar.write("- CSV Upload")
st.sidebar.write("- Dataset Summary")
st.sidebar.write("- Question Answering")
st.sidebar.write("- Charts")
st.sidebar.write("- Automatic Insights")
st.sidebar.write("- Dataset Cleaning")
st.sidebar.write("- Report Download")
st.sidebar.subheader("AI Settings")
gemini_api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset loaded successfully!")

    rows, columns = df.shape
    required_columns = ["Name", "Age", "City", "Department", "Salary", "Experience"]
    missing_required_columns = [col for col in required_columns if col not in df.columns]

    if missing_required_columns:
        st.warning(
            "Some employee-specific features may not work because these columns are missing: "
            + ", ".join(missing_required_columns)
        )
    total_missing = df.isnull().sum().sum()
    duplicate_rows = df.duplicated().sum()

    metric1, metric2, metric3 = st.columns(3)
    metric1.metric("Rows", rows)
    metric2.metric("Columns", columns)
    metric3.metric("Missing Values", total_missing)

    summary_tab, question_tab, ai_tab, chart_tab, cleaning_tab, report_tab = st.tabs([
        "Summary",
        "Questions",
        "Real AI",
        "Charts",
        "Cleaning",
        "Reports"
    ])

    with summary_tab:
        st.subheader("Dataset Preview")
        st.dataframe(df.head())

        st.subheader("Dataset Shape")
        st.write(f"Rows: {rows}")
        st.write(f"Columns: {columns}")

        st.subheader("Column Information")
        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values
        })
        st.dataframe(column_info)

        st.subheader("Numerical Summary")
        st.dataframe(df.describe())

        st.subheader("Automatic Insights")
        st.write(f"The dataset has {rows} rows and {columns} columns.")
        st.write(f"Total missing values in the dataset: {total_missing}")

        numeric_columns = df.select_dtypes(include=["int64", "float64"]).columns
        text_columns = df.select_dtypes(include=["object"]).columns

        if len(numeric_columns) > 0:
            st.write("Numeric columns found:")
            st.write(list(numeric_columns))

            for col in numeric_columns:
                st.write(
                    f"For {col}, average is {df[col].mean():.2f}, "
                    f"minimum is {df[col].min()}, maximum is {df[col].max()}."
                )
        else:
            st.write("No numeric columns found in this dataset.")

        if len(text_columns) > 0:
            st.write("Text/category columns found:")
            st.write(list(text_columns))

            for col in text_columns:
                most_common = df[col].value_counts().idxmax()
                st.write(f"In {col}, the most common value is {most_common}.")

        st.subheader("Dataset Quality Score")

        total_cells = rows * columns

        if total_cells > 0:
            missing_percentage = (total_missing / total_cells) * 100
        else:
            missing_percentage = 0

        quality_score = 100 - missing_percentage - duplicate_rows

        if quality_score < 0:
            quality_score = 0

        st.write(f"Missing values percentage: {missing_percentage:.2f}%")
        st.write(f"Duplicate rows: {duplicate_rows}")
        st.write(f"Dataset quality score: {quality_score:.2f}/100")

    with question_tab:
        st.subheader("Ask a Question About the Dataset")

        question = st.text_input("Type your question here")

        if question:
            question_lower = question.lower()

            if "average salary" in question_lower:
                if "Salary" in df.columns:
                    st.write(f"The average salary is {df['Salary'].mean():.2f}")
                else:
                  st.error("Salary column was not found in this dataset.")

            elif "highest salary" in question_lower:
                if "Salary" in df.columns:
                    st.write(f"The highest salary is {df['Salary'].max()}")
                else:
                    st.error("Salary column was not found in this dataset.")

            elif "lowest salary" in question_lower:
                if "Salary" in df.columns:
                    st.write(f"The lowest salary is {df['Salary'].min()}")
                else:
                    st.error("Salary column was not found in this dataset.")

            elif "average age" in question_lower:
                if "Age" in df.columns:
                    st.write(f"The average age is {df['Age'].mean():.2f}")
                else:
                    st.error("Age column was not found in this dataset.")
            elif "highest age" in question_lower:
                if "Age" in df.columns:
                    st.write(f"The highest age is {df['Age'].max()}")
                else:
                    st.error("Age column was not found in this dataset.")

            elif "total salary" in question_lower:
                if "Salary" in df.columns:
                    st.write(f"The total salary is {df['Salary'].sum()}")
                else:
                    st.error("Salary column was not found in this dataset.")
            elif "lowest age" in question_lower:
                if "Age" in df.columns:
                    st.write(f"The lowest age is {df['Age'].min()}")
                else:
                    st.error("Age column was not found in this dataset.")
            elif "number of employees" in question_lower:
                st.write(f"The total number of employees is {len(df)}.")

            elif "highest experience" in question_lower:
                if "Experience" in df.columns:
                    st.write(f"The highest experience is {df['Experience'].max()} years.")
                else:
                    st.error("Experience column was not found in this dataset.")

            elif "lowest experience" in question_lower:
                if "Experience" in df.columns:
                    st.write(f"The lowest experience is {df['Experience'].min()} years.")
                else:
                    st.error("Experience column was not found in this dataset.")
            elif "average experience" in question_lower:
                if "Experience" in df.columns:
                    st.write(f"The average experience is {df['Experience'].mean():.2f} years.")
                else:
                    st.error("Experience column was not found in this dataset.")


            elif "most employees" in question_lower and "city" in question_lower:
                if "City" in df.columns:
                    city = df["City"].value_counts().idxmax()
                    count = df["City"].value_counts().max()
                    st.write(f"The city with the most employees is {city} with {count} employees.")
                else:
                    st.error("City column was not found in this dataset.")

            elif "most employees" in question_lower and "department" in question_lower:
                if "Department" in df.columns:
                    dept = df["Department"].value_counts().idxmax()
                    count = df["Department"].value_counts().max()
                    st.write(f"The department with the most employees is {dept} with {count} employees.")
                else:
                    st.error("Department column was not found in this dataset.")
            elif "list names" in question_lower or "show names" in question_lower:
                if "Name" in df.columns:
                    st.write("Names in the dataset:")
                    st.dataframe(df["Name"])
                else:
                    st.error("Name column was not found in this dataset.")
            else:
                st.write("Sorry, I cannot answer this question yet.")

        st.subheader("Column Analyzer")

        selected_column = st.selectbox("Choose a column to analyze", df.columns)

        st.write(f"Selected column: {selected_column}")
        st.write("Data type:")
        st.write(df[selected_column].dtype)

        st.write("Missing values:")
        st.write(df[selected_column].isnull().sum())

        if pd.api.types.is_numeric_dtype(df[selected_column]):
            st.write("Average:")
            st.write(df[selected_column].mean())

            st.write("Minimum:")
            st.write(df[selected_column].min())

            st.write("Maximum:")
            st.write(df[selected_column].max())
        else:
            st.write("Most common values:")
            st.dataframe(df[selected_column].value_counts().head(10))

        st.subheader("Search Dataset")

        search_text = st.text_input("Search any value in the dataset")

        if search_text:
            search_results = df[
                df.astype(str).apply(
                    lambda row: row.str.contains(search_text, case=False, na=False).any(),
                    axis=1
                )
            ]

            st.write(f"Found {len(search_results)} matching rows")
            st.dataframe(search_results)

        st.subheader("Filter Dataset by Column")

        filter_column = st.selectbox("Choose column for filter", df.columns)
        unique_values = df[filter_column].dropna().unique()
        selected_value = st.selectbox("Choose value", unique_values)

        filtered_df = df[df[filter_column] == selected_value]

        st.write(f"Showing rows where {filter_column} = {selected_value}")
        st.dataframe(filtered_df)

        filtered_csv = filtered_df.to_csv(index=False)

        st.download_button(
            label="Download Filtered CSV",
            data=filtered_csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
        with ai_tab:
         st.subheader("Ask Real AI About Your Dataset")

         ai_question = st.text_area("Ask any question about the uploaded dataset")

         if st.button("Ask Gemini AI"):
            if not gemini_api_key:
                st.error("Please enter your Gemini API key in the sidebar.")
            elif not ai_question:
                st.error("Please type a question.")
            else:
                try:
                    client = genai.Client(api_key=gemini_api_key)

                    dataset_summary = f"""
Dataset columns: {list(df.columns)}
Dataset shape: {df.shape}

Data types:
{df.dtypes.to_string()}

Missing values:
{df.isnull().sum().to_string()}

Numerical summary:
{df.describe().to_string()}

First 10 rows:
{df.head(10).to_string()}
"""

                    prompt = f"""
You are an AI Data Analyst.

Use the dataset summary below to answer the user's question.
Do not make up numbers.
If the answer cannot be found from the provided dataset summary,
say that more data or calculation is needed.

Dataset summary:
{dataset_summary}

User question:
{ai_question}
"""

                    response = client.models.generate_content(
                        model="gemini-2.5-flash",
                        contents=prompt
                    )

                    st.subheader("AI Answer")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"AI error: {e}")   

    with chart_tab:
        st.subheader("Data Visualization")

        chart_option = st.selectbox(
            "Choose a chart",
            ["Employees by City", "Employees by Department", "Salary by Name"]
        )

        if chart_option == "Employees by City":
            st.bar_chart(df["City"].value_counts())

        elif chart_option == "Employees by Department":
            st.bar_chart(df["Department"].value_counts())

        elif chart_option == "Salary by Name":
            st.bar_chart(df.set_index("Name")["Salary"])

        st.subheader("Custom Chart Generator")

        numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
        all_cols = df.columns.tolist()

        chart_type = st.selectbox("Select chart type", ["Bar Chart", "Line Chart"])
        x_column = st.selectbox("Select X-axis column", all_cols)

        if numeric_cols:
            y_column = st.selectbox("Select Y-axis numeric column", numeric_cols)
            chart_data = df[[x_column, y_column]].dropna()

            if chart_type == "Bar Chart":
                st.bar_chart(chart_data.set_index(x_column))

            elif chart_type == "Line Chart":
                st.line_chart(chart_data.set_index(x_column))
        else:
            st.warning("No numeric columns found for chart generation.")

        st.subheader("Correlation Analysis")

        numeric_df = df.select_dtypes(include=["int64", "float64"])

        if not numeric_df.empty:
            st.dataframe(numeric_df.corr())
        else:
            st.info("No numeric columns available for correlation analysis.")

    with cleaning_tab:
        st.subheader("Dataset Cleaning")

        cleaned_df = df.copy()

        if st.button("Remove Duplicate Rows"):
            cleaned_df = cleaned_df.drop_duplicates()
            st.success("Duplicate rows removed.")
            st.dataframe(cleaned_df)

        if st.button("Fill Missing Numeric Values with Average"):
            numeric_cols = cleaned_df.select_dtypes(include=["int64", "float64"]).columns
            cleaned_df[numeric_cols] = cleaned_df[numeric_cols].fillna(cleaned_df[numeric_cols].mean())
            st.success("Missing numeric values filled with average.")
            st.dataframe(cleaned_df)

        st.subheader("Download Cleaned Dataset")

        cleaned_csv = cleaned_df.to_csv(index=False)

        st.download_button(
            label="Download Cleaned CSV",
            data=cleaned_csv,
            file_name="cleaned_dataset.csv",
            mime="text/csv"
        )

    with report_tab:
        st.subheader("Download Dataset Summary")

        column_info = pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.astype(str),
            "Missing Values": df.isnull().sum().values
        })

        summary_text = f"""
AI Data Analyst Report

Rows: {rows}
Columns: {columns}

Column Information:
{column_info.to_string(index=False)}

Numerical Summary:
{df.describe().to_string()}
"""

        st.download_button(
            label="Download Summary Report",
            data=summary_text,
            file_name="dataset_summary.txt",
            mime="text/plain"
        )

        st.subheader("Project Status")

        st.write("This AI Data Analyst Agent can currently:")
        st.write("- Upload and read CSV files")
        st.write("- Show dataset preview")
        st.write("- Show rows and columns")
        st.write("- Show data types and missing values")
        st.write("- Show numerical summary")
        st.write("- Answer basic salary, city, and department questions")
        st.write("- Create simple charts")
        st.write("- Clean datasets")
        st.write("- Download reports")

        st.subheader("Final Conclusion")

        if quality_score >= 80:
            st.success("The dataset quality is good and ready for analysis.")
        elif quality_score >= 50:
            st.warning("The dataset is usable, but it needs some cleaning before deep analysis.")
        else:
            st.error("The dataset quality is low. Please clean missing values and duplicate rows before analysis.")

        st.subheader("AI Recommendations")

        recommendations = []

        if total_missing > 0:
            recommendations.append("The dataset has missing values. You should clean or fill them before advanced analysis.")

        if duplicate_rows > 0:
            recommendations.append("The dataset has duplicate rows. Removing duplicates can improve analysis quality.")

        if len(numeric_columns) > 0:
            recommendations.append("Numeric columns are available, so this dataset can be used for statistical analysis and charts.")

        if len(text_columns) > 0:
            recommendations.append("Text or category columns are available, so grouping and comparison analysis can be performed.")

        if len(recommendations) == 0:
            recommendations.append("The dataset looks clean and ready for analysis.")

        for rec in recommendations:
            st.write(f"- {rec}")

        st.subheader("About This Project")

        st.write("""
        This project is an AI Data Analyst Agent built using Python, Streamlit, and Pandas.
        It allows users to upload CSV files, understand datasets, ask basic questions,
        generate charts, clean data, search and filter records, download reports, and get
        automatic insights and recommendations.
        """)

else:
    st.info("Please upload a CSV file to begin.")