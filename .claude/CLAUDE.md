<!-- Import workspace-level CLAUDE.md configuration -->
<!-- See /home/lab/workspace/.claude/CLAUDE.md for complete rules -->

# Project-Specific Configuration

This file extends workspace-level configuration with project-specific rules.

## Project Context

**streamlit-chat-with-fileupload** - A Streamlit custom component providing a chat input box with integrated file upload widget.

**Technology Stack**:
- Python 3.12
- Streamlit (custom components)
- loguru for logging
- typer for CLI
- python-dotenv for environment configuration
- pytest for testing
- ruff for linting and formatting

**Project Structure**:
- `lib_streamlit_chat_with_fileupload/` - Main source code module
  - `config.py` - Configuration and variables
  - `dataset.py` - Data handling scripts
  - `features.py` - Feature engineering code
  - `plots.py` - Visualization utilities
  - `modeling/` - ML model training and inference
- `tests/` - Test suite
- `notebooks/` - Jupyter notebooks for exploration
- `models/` - Trained model artifacts
- `docs/` - Documentation (mkdocs)
- `reports/` - Generated analysis outputs

**Naming Conventions**:
- Module prefix: `lib_streamlit_chat_with_fileupload`
- Use snake_case for Python files and functions
- Follow cookiecutter-data-science project template conventions

## Data Science Project Rules

This project follows the cookiecutter-data-science template. When working with data science tasks:
- Raw data goes in `data/raw/` (immutable)
- Processed data goes in `data/processed/`
- Intermediate transformations go in `data/interim/`
- External data sources go in `data/external/`
- Use the Makefile for common operations
