import streamlit as st
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import plotly.express as px
import ollama  # DeepSeek LLM API

# Set Page Configuration
st.set_page_config(page_title="Log Analyzer with AI", layout="wide")

# Path to dataset folder
DATASET_DIR = "/home/intern/Downloads"  # Corrected path format

st.title("?? AI-Powered Log Analysis Using DeepSeek LLM")

# Function to get all CSV files dynamically
def get_datasets():
    files = glob.glob(os.path.join(DATASET_DIR, "*.csv"))
    dataset_dict = {os.path.basename(f).replace(".csv", ""): f for f in files}
    return dataset_dict

# Get available datasets
datasets = get_datasets()

# Allow user to upload new dataset
uploaded_file = st.file_uploader("?? Upload a New Dataset (CSV File)", type=["csv"])
if uploaded_file:
    new_file_path = os.path.join(DATASET_DIR, uploaded_file.name)
    with open(new_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"? New dataset '{uploaded_file.name}' uploaded successfully! Refresh to see it in the dropdown.")

# Dropdown to select dataset
if datasets:
    dataset_name = st.selectbox("?? Select a Dataset", list(datasets.keys()))
    file_path = datasets[dataset_name]

    # Load selected dataset
    try:
        df = pd.read_csv(file_path)
        st.success(f"? Loaded '{dataset_name}' dataset successfully!")

        # Ensure Timestamp column exists
        if "Timestamp" not in df.columns:
            st.warning("?? No 'Timestamp' column found! Creating one automatically.")
            df["Timestamp"] = pd.date_range(start='1/1/2024', periods=len(df), freq='S')
        else:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors='coerce')

        # Show dataset preview
        st.write("### ?? Dataset Overview")
        st.dataframe(df.head(20), use_container_width=True)

        # Select column for visualization
        selected_column = st.selectbox("?? Select a Column for Visualization", df.columns)

        # Generate Histogram with Plotly
        st.write(f"### ?? Distribution of '{selected_column}'")
        fig = px.histogram(df, x=selected_column, nbins=30, title=f"Distribution of {selected_column}")
        st.plotly_chart(fig, use_container_width=True)

        # **Log Activity Graph**
        st.write("### ?? Log Activity Over Time")
        df["hour"] = df["Timestamp"].dt.hour
        log_counts = df["hour"].value_counts().sort_index()
        
        fig, ax = plt.subplots(figsize=(10, 5))
        log_counts.plot(kind="bar", color="skyblue", ax=ax)
        ax.set_xlabel("Hour of the Day")
        ax.set_ylabel("Log Count")
        ax.set_title("Log Activity Over Time")
        st.pyplot(fig)

        # **AI-Powered Log Analysis**
        st.write("### ?? AI Chatbot for Log Analysis")
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("?? Ask about the logs (e.g., anomalies, traffic patterns)..."):
            st.session_state.messages.append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            # **DeepSeek LLM Processing**
            try:
                # Convert dataset to text for model input
                sample_data = df.head(100).to_string()
                llm_prompt = f"""
                You are an AI analyzing network log data.
                The user asked: '{prompt}'
                Below is a sample of the log dataset:
                {sample_data}
                Provide an insightful answer based on the logs.
                """

                # Query DeepSeek LLM using Ollama
                response = ollama.chat(model="deepseek", messages=[{"role": "user", "content": llm_prompt}])

                # Extract and format response
                response_text = response["message"]["content"]

            except Exception as e:
                response_text = f"?? Error analyzing logs: {e}"

            # Display response
            with st.chat_message("assistant"):
                st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

    except Exception as e:
        st.error(f"? Error loading dataset: {e}")

else:
    st.warning("?? No datasets found! Please upload one.")