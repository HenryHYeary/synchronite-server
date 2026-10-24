import os

from dotenv import load_dotenv

load_dotenv()

def _require(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {value}")
    return value

DATABASE_URL = _require("DATABASE_URL")

