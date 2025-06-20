import os
from dotenv import load_dotenv


def test_env_variable_loaded():
    """Ensure GOOGLE_APPLICATION_CREDENTIALS from .env is loaded."""
    load_dotenv()
    assert os.getenv("GOOGLE_APPLICATION_CREDENTIALS") is not None
