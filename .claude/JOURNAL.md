# Claude Code Journal

This journal tracks substantive work on documents, diagrams, and documentation content.

---

1. **Task - Project initialization setup**: Created `.claude/` directory with CLAUDE.md and JOURNAL.md configuration files<br>
   **Result**: Initialized project-level Claude Code configuration importing workspace-level rules from `/home/lab/workspace/.claude/CLAUDE.md`. Created `CLAUDE.md` documenting the project context including Python 3.12, Streamlit custom components, and cookiecutter-data-science template structure. The project is a chat input widget with file upload capability for Streamlit applications.

2. **Task - Streamlit Claude chat client**: Researched Streamlit custom components and Anthropic SDK, built simple chat client<br>
   **Result**: Used Context7 to fetch current Streamlit docs on custom components (v1/v2 APIs, `st.chat_input`, `st.chat_message`) and Anthropic Python SDK streaming patterns. Cleaned up `lib_streamlit_chat_with_fileupload/` by removing `dataset.py`, `features.py`, `plots.py`, and `modeling/` directory - kept only `config.py` and `__init__.py`. Simplified `config.py` to load `ANTHROPIC_API_KEY` from environment with `CLAUDE_MODEL` set to `claude-sonnet-4-20250514` and `MAX_TOKENS=4096`. Created `.env` template with `ANTHROPIC_API_KEY=your-api-key-here`. Updated `pyproject.toml` dependencies to `anthropic`, `python-dotenv`, and `streamlit`. Created `app.py` implementing a basic chat interface using `st.chat_input` for user prompts, `st.chat_message` for message display, `st.session_state.messages` for history persistence, and synchronous `client.messages.create()` for Claude responses.

3. **Task - Switch to AWS Bedrock**: Migrated chat app from direct Anthropic API to AWS Bedrock with model selection<br>
   **Result**: Updated `config.py` to use `AWS_PROFILE=kolomolo` and `AWS_REGION=us-east-1` from environment, added `CLAUDE_MODELS` dict with five options (Claude 3.5 Sonnet, Claude 3.5 Haiku, Claude 3.7 Sonnet, Claude 4 Sonnet, Claude 4 Opus) mapping display names to Bedrock model IDs. Rewrote `app.py` to use boto3 `bedrock-runtime` client with `converse()` API instead of Anthropic SDK. Added sidebar with model selector dropdown and "Clear Chat" button. Messages converted to Bedrock format `{"role": ..., "content": [{"text": ...}]}`. Updated `pyproject.toml` dependencies replacing `anthropic` with `boto3`. Updated `.env` with `AWS_PROFILE=kolomolo` and `AWS_REGION=us-east-1`.
