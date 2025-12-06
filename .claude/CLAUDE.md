<!-- Import workspace-level CLAUDE.md configuration -->
<!-- See /home/lab/workspace/.claude/CLAUDE.md for complete rules -->

# Project-Specific Configuration

This file extends workspace-level configuration with project-specific rules.

## Project Context

**streamlit-chat-input-fileupload** - A Streamlit custom component providing a chat input box with integrated file upload widget.

**Technology Stack**:
- Python 3.12
- Streamlit (custom components v2 API)
- python-dotenv for environment configuration
- boto3 for AWS Bedrock integration (demo app)
- pytest for testing
- ruff for linting and formatting

**Project Structure**:
- `streamlit_chat_input_fileupload/` - Main source code module
  - `__init__.py` - Package exports
  - `config.py` - Configuration and variables
  - `chat_input_with_upload/` - Custom component implementation
- `app.py` - Demo application with AWS Bedrock chat
- `tests/` - Test suite

**Naming Conventions**:
- PyPI package: `streamlit-chat-input-fileupload`
- Module: `streamlit_chat_input_fileupload`
- Use snake_case for Python files and functions
