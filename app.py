"""Streamlit chat application with Claude via AWS Bedrock."""

import boto3
import streamlit as st
from botocore.exceptions import ClientError

from lib_streamlit_chat_with_fileupload.config import (
    AWS_PROFILE,
    AWS_REGION,
    CLAUDE_MODELS,
    DEFAULT_MODEL,
    MAX_TOKENS,
)

st.set_page_config(
    page_title="Claude Chat",
    page_icon="🤖",
    layout="centered",
)

st.title("Claude Chat")


@st.cache_resource
def get_bedrock_client():
    """Initialize and cache Bedrock Runtime client."""
    session = boto3.Session(profile_name=AWS_PROFILE)
    return session.client("bedrock-runtime", region_name=AWS_REGION)


client = get_bedrock_client()

# Sidebar for model selection
with st.sidebar:
    st.header("Settings")
    selected_model = st.selectbox(
        "Model",
        options=list(CLAUDE_MODELS.keys()),
        index=list(CLAUDE_MODELS.keys()).index(DEFAULT_MODEL),
    )
    model_id = CLAUDE_MODELS[selected_model]
    st.caption(f"Model ID: `{model_id}`")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Send a message..."):
    # Add user message to history and display
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Convert messages to Bedrock Converse format
    bedrock_messages = [
        {"role": msg["role"], "content": [{"text": msg["content"]}]}
        for msg in st.session_state.messages
    ]

    # Generate response from Claude via Bedrock
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.converse(
                    modelId=model_id,
                    messages=bedrock_messages,
                    inferenceConfig={"maxTokens": MAX_TOKENS},
                )
                assistant_message = response["output"]["message"]["content"][0]["text"]
            except ClientError as e:
                assistant_message = f"Error: {e}"
                st.error(assistant_message)

        st.markdown(assistant_message)

    # Add assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
