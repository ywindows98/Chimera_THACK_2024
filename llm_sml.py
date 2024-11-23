# RUN WITH:
# streamlit run llm_sml.py --server.address 127.0.0.1

# RUN WITH:
# streamlit run llm_sml.py --server.address 127.0.0.1

import streamlit as st
from streamlit_chat import message
import pandas as pd
import json


# Page Configuration
st.set_page_config(
    page_title="Chimera LLM",
    layout="centered",
)

# Title
st.title("Chimera LLM Chat")

# Initialize Chat History and Uploaded Data in Session State
if "messages" not in st.session_state:
    st.session_state.messages = []
if "uploaded_data" not in st.session_state:
    st.session_state.uploaded_data = None

# Input handler function
def handle_message():
    query = st.session_state["user_input"]
    if query.strip():
        # Add the user's message to the session state
        st.session_state.messages.append({"role": "user", "content": query})

        # Prepare payload with optional uploaded data for potential backend
        payload = {"query": query}
        if st.session_state.uploaded_data is not None:
            payload["file_data"] = st.session_state.uploaded_data

        st.session_state.messages.append({"role": "bot", "content": f"Response to: {payload['query']}"})

        # Clear the input field
        st.session_state["user_input"] = ""

# File upload handler
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        try:
            # Handle CSV files
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file)

            # Handle JSON files
            elif uploaded_file.name.endswith(".json"):
                data = json.load(uploaded_file)
                df = pd.DataFrame(data)

            st.success(f"File '{uploaded_file.name}' uploaded successfully!")
        except Exception as e:
            st.error(f"Error processing file: {e}")

# File Upload Section
st.sidebar.header("📂 Upload a File")
uploaded_file = st.sidebar.file_uploader(
    "Upload a CSV or JSON file",
    type=["csv", "json"],
    on_change=lambda: handle_file_upload(uploaded_file)
)

# Chat Input Section
if "user_input" not in st.session_state:
    st.session_state["user_input"] = ""  # Initialize input field in session state

st.text_area(
    "Your question:",
    value=st.session_state["user_input"],
    placeholder="Ask me anything...",
    height=70,
    key="user_input",
    on_change=handle_message  # Trigger when Enter is pressed
)

# Display Chat History (Newest on Top)
st.subheader("💬 Chat History")
for i, msg in enumerate(reversed(st.session_state.messages)):  # Reverse the message list
    if msg["role"] == "user":
        message(msg["content"], is_user=True, key=f"user-{len(st.session_state.messages) - i}")
    else:
        message(msg["content"], key=f"bot-{len(st.session_state.messages) - i}")

































