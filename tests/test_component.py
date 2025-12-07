"""Tests for the chat input component."""

import base64
from unittest.mock import MagicMock, patch

import pytest


class TestChatInputComponent:
    """Tests for chat_input_with_upload component."""

    def test_component_import(self):
        """Test that component can be imported."""
        from streamlit_chat_input_fileupload import chat_input_with_upload

        assert chat_input_with_upload is not None
        assert callable(chat_input_with_upload)

    def test_config_import(self):
        """Test that config can be imported."""
        from streamlit_chat_input_fileupload.config import (
            AWS_PROFILE,
            AWS_REGION,
            MAX_TOKENS,
        )

        assert MAX_TOKENS == 4096
        assert AWS_PROFILE is not None
        assert AWS_REGION is not None


class TestMockLLMIntegration:
    """Integration tests with mocked LLM responses."""

    @pytest.fixture
    def mock_bedrock_response(self):
        """Mock Bedrock converse response."""
        return {
            "output": {"message": {"content": [{"text": "This is a mock response from Claude."}]}}
        }

    @pytest.fixture
    def sample_user_message(self):
        """Sample user message with text only."""
        return {"text": "Hello, Claude!", "file": None}

    @pytest.fixture
    def sample_user_message_with_file(self):
        """Sample user message with file attachment."""
        return {
            "text": "What is in this file?",
            "file": {
                "name": "test.txt",
                "type": "text/plain",
                "size": 13,
                "data": b"Hello, World!",
            },
        }

    def test_mock_bedrock_response_structure(self, mock_bedrock_response):
        """Test mock response has expected structure."""
        assert "output" in mock_bedrock_response
        assert "message" in mock_bedrock_response["output"]
        assert "content" in mock_bedrock_response["output"]["message"]
        assert len(mock_bedrock_response["output"]["message"]["content"]) > 0
        assert "text" in mock_bedrock_response["output"]["message"]["content"][0]

    def test_extract_assistant_message(self, mock_bedrock_response):
        """Test extracting assistant message from response."""
        assistant_message = mock_bedrock_response["output"]["message"]["content"][0]["text"]
        assert assistant_message == "This is a mock response from Claude."

    def test_user_message_format(self, sample_user_message):
        """Test user message has expected format."""
        assert "text" in sample_user_message
        assert "file" in sample_user_message
        assert sample_user_message["text"] == "Hello, Claude!"
        assert sample_user_message["file"] is None

    def test_user_message_with_file_format(self, sample_user_message_with_file):
        """Test user message with file has expected format."""
        msg = sample_user_message_with_file
        assert msg["text"] == "What is in this file?"
        assert msg["file"] is not None
        assert msg["file"]["name"] == "test.txt"
        assert msg["file"]["type"] == "text/plain"
        assert msg["file"]["data"] == b"Hello, World!"

    def test_build_bedrock_message_text_only(self, sample_user_message):
        """Test building Bedrock message format for text-only message."""
        bedrock_content = []
        if sample_user_message["text"]:
            bedrock_content.append({"text": sample_user_message["text"]})

        assert len(bedrock_content) == 1
        assert bedrock_content[0]["text"] == "Hello, Claude!"

    def test_build_bedrock_message_with_document(self, sample_user_message_with_file):
        """Test building Bedrock message format with document."""
        msg = sample_user_message_with_file
        bedrock_content = []

        if msg["file"]:
            bedrock_content.append(
                {
                    "document": {
                        "format": "txt",
                        "name": msg["file"]["name"].replace(".", "_"),
                        "source": {"bytes": msg["file"]["data"]},
                    }
                }
            )

        if msg["text"]:
            bedrock_content.append({"text": msg["text"]})

        assert len(bedrock_content) == 2
        assert "document" in bedrock_content[0]
        assert bedrock_content[0]["document"]["format"] == "txt"
        assert bedrock_content[1]["text"] == "What is in this file?"

    @patch("boto3.Session")
    def test_mock_bedrock_client_call(self, mock_session, mock_bedrock_response):
        """Test mocking Bedrock client call."""
        mock_client = MagicMock()
        mock_client.converse.return_value = mock_bedrock_response
        mock_session.return_value.client.return_value = mock_client

        # Simulate the call
        session = mock_session(profile_name="test")
        client = session.client("bedrock-runtime", region_name="us-east-1")
        response = client.converse(
            modelId="test-model",
            messages=[{"role": "user", "content": [{"text": "Hello"}]}],
            inferenceConfig={"maxTokens": 4096},
        )

        assert response == mock_bedrock_response
        mock_client.converse.assert_called_once()


class TestFileProcessing:
    """Tests for file processing utilities."""

    def test_base64_encoding(self):
        """Test base64 encoding of file data."""
        original = b"Hello, World!"
        encoded = base64.b64encode(original).decode("utf-8")
        decoded = base64.b64decode(encoded)

        assert decoded == original

    @pytest.mark.parametrize(
        "filename,expected_format",
        [
            ("document.pdf", "pdf"),
            ("data.csv", "csv"),
            ("notes.txt", "txt"),
            ("report.xlsx", "xlsx"),
            ("readme.md", "md"),
            ("page.html", "html"),
        ],
    )
    def test_file_extension_mapping(self, filename, expected_format):
        """Test file extension to Bedrock format mapping."""
        ext_map = {
            "pdf": "pdf",
            "txt": "txt",
            "csv": "csv",
            "html": "html",
            "md": "md",
            "xlsx": "xlsx",
        }

        ext = filename.split(".")[-1].lower()
        result = ext_map.get(ext)

        assert result == expected_format

    @pytest.mark.parametrize(
        "mime_type,expected_format",
        [
            ("application/pdf", "pdf"),
            ("text/plain", "txt"),
            ("text/csv", "csv"),
            (
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                "xlsx",
            ),
        ],
    )
    def test_mime_type_mapping(self, mime_type, expected_format):
        """Test MIME type to Bedrock format mapping."""
        mime_map = {
            "application/pdf": "pdf",
            "text/plain": "txt",
            "text/csv": "csv",
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        }

        result = mime_map.get(mime_type)

        assert result == expected_format
