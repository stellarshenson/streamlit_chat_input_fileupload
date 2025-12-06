import os
from pathlib import Path

from dotenv import load_dotenv

# Load environment variables from .env file if it exists
load_dotenv()

# paths
PROJ_ROOT = Path(__file__).resolve().parents[1]

# AWS configuration
AWS_PROFILE = os.getenv("AWS_PROFILE", "kolomolo")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Bedrock Claude inference profile ARNs
CLAUDE_MODELS = {
    "haiku": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/us.anthropic.claude-3-5-haiku-20241022-v1:0",
    "sonnet": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/us.anthropic.claude-3-5-sonnet-20241022-v2:0",
    "sonnet-3.7": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
    "sonnet-4": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/us.anthropic.claude-sonnet-4-20250514-v1:0",
    "sonnet-4.5": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/us.anthropic.claude-sonnet-4-5-20250929-v1:0",
    "opus": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/us.anthropic.claude-opus-4-20250514-v1:0",
    "opus-4.5": "arn:aws:bedrock:us-east-1:067710371089:inference-profile/global.anthropic.claude-opus-4-5-20251101-v1:0",
}

DEFAULT_MODEL = "sonnet-3.7"
MAX_TOKENS = 4096
