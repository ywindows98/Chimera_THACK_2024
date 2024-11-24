# RUN WITH:
# streamlit run llm_sml.py --server.address 127.0.0.1

import streamlit as st
from streamlit_chat import message
import pandas as pd
import json
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os
from llm_func import use_llm
from convert_files import Converter
from database import create_db, add_code_to_db

if "initialized" not in st.session_state:
    st.session_state.initialized = True
    create_db()  # Create Database
    # Initialize Chat History and Uploaded Data in Session State
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "uploaded_data" not in st.session_state:
        st.session_state.uploaded_data = None
    if "current_index" not in st.session_state:
        st.session_state.current_index = 0
    if "plots" not in st.session_state:
        st.session_state.plots = []
    if "prev_disabled" not in st.session_state:
        st.session_state.prev_disabled = True
    if "next_disabled" not in st.session_state:
        st.session_state.next_disabled = True
    if "liked" not in st.session_state:
        st.session_state.liked = False
    if "disliked" not in st.session_state:
        st.session_state.disliked = False
    if "code_added" not in st.session_state:
        st.session_state.code_added = False

#  "👍"
def like():
    st.session_state.liked = True
    st.session_state.disliked = False

    if not st.session_state.code_added:
        file_name = "response_output.py"
        gpt_code = str()
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                gpt_code += line.strip()
        add_code_to_db(st.session_state["query"], gpt_code)
        st.session_state.code_added = True

#  "👎"
def dislike():
    st.session_state.liked = False
    st.session_state.disliked = True


def read_plots(folder_path):
    # List to hold images
    images = []
    plots = []

    # Check for PNG files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.png'):
            file_path = os.path.join(folder_path, file_name)
            # Read and store the image using matplotlib
            img = mpimg.imread(file_path)
            images.append((file_name, img))
            # print(f"Loaded: {file_name}")

    # Display the images
    for file_name, img in images:
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(img)
        ax.axis('off')  # Turn off axis labels
        fig.patch.set_alpha(0.0)  # Figure background
        ax.patch.set_alpha(0.0)  # Axes background
        ax.set_title(f"{file_name}")
        plots.append(fig)

    st.session_state.plots = plots


# Input handler function
def handle_message(is_new_query: bool = True):
    if not os.path.exists("current_data.csv"):
        st.session_state.messages.append({"role": "bot", "content": f"Please upload a file to use an assistant"})
    else:
        if is_new_query:
            query = st.session_state["user_input"]
            use_llm(query)
            st.session_state["query"] = ""  # Clear the previous query
            st.session_state.code_added = False # Reset the code added flag
        else:
            query = st.session_state["query"]
            add_new_query = "Based on the previous request, please create a new graph with a different visualization style or perspective. Here's the original request: "
            add_new_query += query
            use_llm(add_new_query)
            st.session_state.code_added = False

        read_plots('figures')
        if query.strip():
            # Add the user's message to the session state
            st.session_state.messages.append({"role": "user", "content": query})

            # Prepare payload with optional uploaded data for potential backend
            payload = {"query": query}
            if st.session_state.uploaded_data is not None:
                payload["file_data"] = st.session_state.uploaded_data

            # Mock response
            st.session_state.messages.append({"role": "bot", "content": f"Response to: {payload['query']}"})

            # Clear the input field
            if is_new_query:
                st.session_state["query"] = query
                st.session_state["user_input"] = ""


# File upload handler
def handle_file_upload(uploaded_file):
    if uploaded_file is not None:
        try:
            # Handle CSV files
            # if uploaded_file.name.endswith(".csv"):
            #     df = pd.read_csv(uploaded_file)
            #     df.to_csv("current_data.csv", index=False)

            # Handle JSON files
            # elif uploaded_file.name.endswith(".json"):
            #     data = json.load(uploaded_file)
            #     df = pd.DataFrame(data)
            #     df.to_csv("current_data.csv", index=False)

            # Saving the uploaded file
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())

            # Getting file path and format
            file_path = uploaded_file.name
            file_format = '.' + file_path.split('.')[-1]

            # Convert file to txt
            if file_format == 'pdf' or file_format == 'docx':
                _ = Converter.pdf_to_txt(uploaded_file, "current_data.txt")
                df, _, _ = Converter.file_to_dataframe("current_data.txt", "txt")
                df.to_csv("current_data.csv", index=False)
            else:
                df, _, _ = Converter.file_to_dataframe(file_path, file_format)
                df.to_csv("current_data.csv", index=False)

            st.session_state.uploaded_data = df  # Store uploaded data in session state
            st.sidebar.success(f"File '{uploaded_file.name}' uploaded successfully!")
        except Exception as e:
            st.sidebar.error(f"Error processing file: {e}")


# This function is used to update the plot using session data
def update_plot_from_session():
    if st.session_state.uploaded_data is not None:
        st.write("Data Preview:")
        st.dataframe(st.session_state.uploaded_data.head())  # Display the first few rows of the data

        st.write("Visualization Placeholder:")
        # Example: Plotting a simple histogram
        if isinstance(st.session_state.uploaded_data, pd.DataFrame):
            numeric_columns = st.session_state.uploaded_data.select_dtypes(include=['number']).columns
            if not numeric_columns.empty:
                column_to_plot = st.selectbox("Select a column to plot:", numeric_columns)
                st.bar_chart(st.session_state.uploaded_data[column_to_plot])
            else:
                st.warning("No numeric columns available for plotting.")
    else:
        st.info("Upload a file to see data and plots.")


# Function to display the passed figure
def display_plot(fig):
    if fig is not None:
        st.pyplot(fig)
    else:
        st.warning("No figure provided to display.")


# Main Area for Plotting
# st.header("Plotting Area")

# Page Configuration
st.set_page_config(
    page_title="Chimera LLM",
    layout="wide",  # Allows more space for plots
    page_icon="images/logo_min.jpg"
)

st.markdown(
    """
    <style>
    .stFileUploader label {
        display: none;  /* Hide the label */
    }

    .stTextArea label {
        display: none;  /* Hide the label */
    }

    .stChatMessage {
        background-color: rgba(255, 255, 255, 0.0);  /* Hide the label */
    }

    .stColumn {
                text-align:center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title
st.title("🦁 Chimera LLM Chat ")

# read_plots('prototype/figures')
# simulate_test_plots()


# Sidebar for File Upload and Chat
with st.sidebar:
    # File Upload Section
    uploaded_file = st.file_uploader(
        "",
        # "Upload a CSV, JSON, PDF, TXT, XLSX or DOCX",
        type=["csv", "json", "pdf", "txt", "xlsx", "docx"]
    )

    # Trigger file upload processing after the file is selected
    if uploaded_file is not None:
        handle_file_upload(uploaded_file)

    # Chat Input Section
    st.subheader("💬 Chat")
    if "user_input" not in st.session_state:
        st.session_state["user_input"] = ""  # Initialize input field in session state
    if "query" not in st.session_state:
        st.session_state["query"] = False
    

    st.text_area(
        "",
        # "Your question:",
        value=st.session_state["user_input"],
        placeholder="Make a request...",
        height=70,
        key="user_input",
        on_change=handle_message  # Trigger when Enter is pressed
    )

    # Display Chat History (Newest on Top)
    st.subheader("🗨️ Chat History")
    for i, msg in enumerate(reversed(st.session_state.messages)):  # Reverse the message list
        if msg["role"] == "user":
            user_avatar = "../images/logo_min.jpg"
            with st.chat_message('User'):
                st.write(msg["content"])
        else:
            bot_avatar = "../images/logo_min.jpg"
            with st.chat_message('Bot', avatar=bot_avatar):
                st.write(msg["content"])

if st.session_state.current_index > 0:
    st.session_state.prev_disabled = False
else:
    st.session_state.prev_disabled = True

if st.session_state.current_index < len(st.session_state.plots) - 1:
    st.session_state.next_disabled = False
else:
    st.session_state.next_disabled = True

# Buttons to switch between figures
col1, col2 = st.columns([1, 1])  # Create two columns for the buttons
with col1:
    if st.button("Previous Figure", disabled=st.session_state.prev_disabled):
        if st.session_state.current_index > 0:
            st.session_state.current_index -= 1
        st.rerun()

with col2:
    if st.button("Next Figure", disabled=st.session_state.next_disabled):
        if st.session_state.current_index < len(st.session_state.plots) - 1:
            st.session_state.current_index += 1
        st.rerun()

# Display the current figure
if len(st.session_state.plots) > 0:
    fig = st.session_state.plots[st.session_state.current_index]
    st.pyplot(fig)

    col3, col4, col5, _ = st.columns([1, 1, 0.5, 5])
    with col3:
        # Buttons for regenerate
        if st.button("Regenerate Figures", on_click=like):

            handle_message(False)
            st.rerun()
    with col4:
        if st.button("👍", on_click=like):
            st.write("You liked the figure!")
    with col5:
        if st.button("👎", on_click=dislike):
            st.write("You disliked the figure!")
    

