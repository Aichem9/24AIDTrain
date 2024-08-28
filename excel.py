import streamlit as st
import pandas as pd
import openai
from dotenv import load_dotenv
import os

# Load environment variables, including API keys
load_dotenv()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

st.title("📊 엑셀 데이터 분석 및 GPT 피드백 생성기 📝")

# Initialize session state for messages and analysis chain
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "analysis_chain" not in st.session_state:
    st.session_state["analysis_chain"] = None

# Sidebar for file upload and model selection
with st.sidebar:
    # Initialization button
    clear_btn = st.button("초기화")

    # Upload Excel file
    uploaded_file = st.file_uploader("파일 업로드", type=["xlsx", "xls"])

    # Select model for summarization and feedback
    selected_model = st.selectbox(
        "LLM 선택", ["gpt-3.5-turbo", "gpt-4"], index=0
    )

    # Button to update settings
    update_btn = st.button("설정 업데이트")

# Function to display previous messages
def print_messages():
    for chat_message in st.session_state["messages"]:
        st.chat_message(chat_message["role"]).write(chat_message["content"])

# Function to add a new message to the session state
def add_message(role, message):
    st.session_state["messages"].append({"role": role, "content": message})

# Function to process and analyze the uploaded Excel file
@st.cache_data(show_spinner="업로드한 파일을 처리 중입니다...")
def analyze_excel(file):
    # Load Excel data into a DataFrame
    df = pd.read_excel(file)
    return df

# Function to create a prompt for GPT
def create_prompt(data_summary):
    prompt = f"""
    Here is a summary of the dataset:

    {data_summary}

    Please provide a detailed analysis and give constructive feedback for improving the dataset.
    """
    return prompt

# Function to query OpenAI API for analysis and feedback
def query_openai(prompt, model="gpt-3.5-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a data analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )
    return response.choices[0].message["content"]

# Process the uploaded file and generate analysis and feedback
if uploaded_file:
    df = analyze_excel(uploaded_file)
    st.write("### 엑셀 데이터:")
    st.write(df)

    # Generate a simple summary of the data
    data_summary = df.describe(include='all').to_string()

    # Create the prompt for GPT
    prompt = create_prompt(data_summary)

    # Query OpenAI's GPT model
    with st.spinner("GPT 모델을 통해 데이터를 분석 중입니다..."):
        gpt_response = query_openai(prompt, model=selected_model)

    st.write("### GPT 피드백:")
    st.write(gpt_response)

    # Save the GPT response in session state
    st.session_state["analysis_chain"] = gpt_response

# Clear previous messages if the button is clicked
if clear_btn:
    st.session_state["messages"] = []
    st.session_state["analysis_chain"] = None

# Update chain settings if the button is clicked
if update_btn and uploaded_file:
    df = analyze_excel(uploaded_file)
    data_summary = df.describe(include='all').to_string()
    prompt = create_prompt(data_summary)
    gpt_response = query_openai(prompt, model=selected_model)
    st.session_state["analysis_chain"] = gpt_response

# Display previous messages
print_messages()

# Input for user queries
user_input = st.chat_input("궁금한 내용을 물어보세요!")

# Process user input and generate response
if user_input:
    if st.session_state["analysis_chain"] is not None:
        st.chat_message("user").write(user_input)

        # Append the user's question to the conversation
        st.session_state["messages"].append({"role": "user", "content": user_input})
        response = query_openai(user_input, model=selected_model)

        with st.chat_message("assistant"):
            container = st.empty()
            container.markdown(response)

        # Save chat history
        add_message("user", user_input)
        add_message("assistant", response)
    else:
        st.error("먼저 파일을 업로드하고 분석을 수행해주세요.")
