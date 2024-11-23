# RUN WITH:
# streamlit run llm_sml.py --server.address 127.0.0.1

import streamlit as st
from streamlit_chat import message
import pandas as pd
import json
import requests

# Flask API URL
FLASK_API_URL = 'http://127.0.0.1:5000/process_llm'  # Local URL, adjust if hosted differently

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

        # Prepare payload with optional uploaded data
        payload = {"query": query}
        if st.session_state.uploaded_data is not None:
            payload["file_data"] = st.session_state.uploaded_data


        # # Send the user input and optional file data to the Flask backend via POST request
        # try:
        #     response = requests.post(FLASK_API_URL, json=payload)
        #     response_json = response.json()
        #     bot_response = response_json.get("response", "Sorry, I couldn't process that.")
        #
        # except requests.exceptions.RequestException as e:
        #     bot_response = "Error: Unable to connect to the backend."

        # # Add the bot's response to the session state
        # st.session_state.messages.append({"role": "bot", "content": bot_response})


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
















