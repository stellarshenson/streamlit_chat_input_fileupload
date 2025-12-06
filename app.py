"""Streamlit chat application with Claude via AWS Bedrock."""

import boto3
import streamlit as st
from botocore.exceptions import ClientError

from lib_streamlit_chat_with_fileupload.chat_input_with_upload import (
    chat_input_with_upload,
)
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
        for content in message["content"]:
            if "text" in content:
                st.markdown(content["text"])
            elif "image" in content:
                st.caption(f"[Image: {content['image'].get('name', 'attached')}]")
            elif "document" in content:
                st.caption(f"[Document: {content['document'].get('name', 'attached')}]")


def get_media_type(file_type: str, file_name: str) -> str:
    """Determine media type from file type or extension."""
    if file_type:
        return file_type

    ext = file_name.lower().split(".")[-1] if "." in file_name else ""
    type_map = {
        "png": "image/png",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "gif": "image/gif",
        "webp": "image/webp",
        "pdf": "application/pdf",
        "txt": "text/plain",
        "csv": "text/csv",
        "json": "application/json",
        "md": "text/markdown",
        "html": "text/html",
        "xml": "application/xml",
    }
    return type_map.get(ext, "application/octet-stream")


def build_content_block(text: str, file_info: dict | None) -> list[dict]:
    """Build Bedrock content block from text and optional file."""
    content = []

    if file_info:
        file_bytes = file_info["data"]
        media_type = get_media_type(file_info["type"], file_info["name"])

        if media_type.startswith("image/"):
            content.append({
                "image": {
                    "format": media_type.split("/")[1],
                    "source": {"bytes": file_bytes},
                    "name": file_info["name"],
                }
            })
        else:
            doc_format = media_type.split("/")[1]
            if doc_format == "plain":
                doc_format = "txt"
            elif doc_format == "markdown":
                doc_format = "md"

            content.append({
                "document": {
                    "format": doc_format,
                    "name": file_info["name"].replace(".", "_"),
                    "source": {"bytes": file_bytes},
                }
            })

    if text:
        content.append({"text": text})

    return content


# Chat input with file upload (custom component)
user_input = chat_input_with_upload(
    placeholder="Send a message...",
    key="chat_input",
)

if user_input:
    text = user_input.get("text", "")
    file_info = user_input.get("file")

    user_content = build_content_block(text, file_info)

    if user_content:
        st.session_state.messages.append({"role": "user", "content": user_content})

        with st.chat_message("user"):
            if file_info:
                st.caption(f"[File: {file_info['name']}]")
            if text:
                st.markdown(text)

        # Build messages for Bedrock API
        bedrock_messages = []
        for msg in st.session_state.messages:
            api_content = []
            for block in msg["content"]:
                if "text" in block:
                    api_content.append({"text": block["text"]})
                elif "image" in block:
                    api_content.append({
                        "image": {
                            "format": block["image"]["format"],
                            "source": {"bytes": block["image"]["source"]["bytes"]},
                        }
                    })
                elif "document" in block:
                    api_content.append({
                        "document": {
                            "format": block["document"]["format"],
                            "name": block["document"]["name"],
                            "source": {"bytes": block["document"]["source"]["bytes"]},
                        }
                    })
            bedrock_messages.append({"role": msg["role"], "content": api_content})

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

        st.session_state.messages.append({
            "role": "assistant",
            "content": [{"text": assistant_message}],
        })

        st.rerun()
