# streamlit-chat-with-fileupload

A Streamlit custom component providing a chat input box with integrated file upload widget.

## Features

- Text input field with send button
- File attachment button (paperclip icon)
- Single file upload at a time
- File indicator showing attached filename with remove option
- Enter key to send, Shift+Enter for newline
- Base64 file encoding for seamless Python integration
- Supports images (png, jpg, gif, webp) and documents (pdf, txt, csv, xlsx, docx, etc.)

## Installation

```bash
pip install lib-streamlit-chat-with-fileupload
```

Or install from source:

```bash
git clone https://github.com/stellars-henson/streamlit-chat-with-fileupload.git
cd streamlit-chat-with-fileupload
pip install -e .
```

## Usage

```python
import streamlit as st
from lib_streamlit_chat_with_fileupload import chat_input_with_upload

# Display the chat input component
user_input = chat_input_with_upload(
    placeholder="Send a message...",
    disabled=False,
    key="chat_input",
)

if user_input:
    text = user_input["text"]
    file_info = user_input["file"]

    st.write(f"Message: {text}")

    if file_info:
        st.write(f"File: {file_info['name']}")
        st.write(f"Size: {file_info['size']} bytes")
        st.write(f"Type: {file_info['type']}")
        # file_info['data'] contains the raw bytes
```

## API Reference

### `chat_input_with_upload()`

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `placeholder` | str | "Send a message..." | Placeholder text for the input field |
| `disabled` | bool | False | Whether the input is disabled |
| `key` | str or None | None | Unique key for the component instance |

**Returns:**

- `None` - When no message has been submitted
- `dict` - When user submits a message:
  - `text` (str): The text message
  - `file` (dict or None): File information if attached
    - `name` (str): Original filename
    - `type` (str): MIME type
    - `size` (int): File size in bytes
    - `data` (bytes): Raw file content

## Example with AWS Bedrock

```python
import boto3
import streamlit as st
from lib_streamlit_chat_with_fileupload import chat_input_with_upload

# Initialize Bedrock client
client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = chat_input_with_upload()

if user_input:
    text = user_input["text"]
    file_info = user_input["file"]

    # Build content for Bedrock
    content = []
    if file_info and file_info["type"].startswith("image/"):
        content.append({
            "image": {
                "format": file_info["type"].split("/")[1],
                "source": {"bytes": file_info["data"]},
            }
        })
    if text:
        content.append({"text": text})

    # Call Bedrock
    response = client.converse(
        modelId="us.anthropic.claude-3-5-sonnet-20241022-v2:0",
        messages=[{"role": "user", "content": content}],
    )

    assistant_text = response["output"]["message"]["content"][0]["text"]
    st.write(assistant_text)
```

## Packaging for Distribution

### Build the package

```bash
# Install build tools
pip install build twine

# Build source and wheel distributions
python -m build

# This creates:
# - dist/lib_streamlit_chat_with_fileupload-0.1.6.tar.gz
# - dist/lib_streamlit_chat_with_fileupload-0.1.6-py3-none-any.whl
```

### Upload to PyPI

```bash
# Upload to TestPyPI first (recommended)
python -m twine upload --repository testpypi dist/*

# Upload to PyPI
python -m twine upload dist/*
```

### Install from PyPI

```bash
pip install lib-streamlit-chat-with-fileupload
```

## Development

```bash
# Clone repository
git clone https://github.com/stellars-henson/streamlit-chat-with-fileupload.git
cd streamlit-chat-with-fileupload

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install in development mode with dev dependencies
pip install -e ".[dev]"

# Run the demo app
make run_streamlit
```

## Project Structure

```
streamlit-chat-with-fileupload/
├── lib_streamlit_chat_with_fileupload/
│   ├── __init__.py
│   ├── config.py
│   └── chat_input_with_upload/
│       └── __init__.py          # Component implementation
├── app.py                        # Demo application
├── pyproject.toml
├── Makefile
└── README.md
```

## Requirements

- Python 3.12+
- Streamlit 1.45+

## License

MIT License
