import os

from dotenv import load_dotenv

from TargetAPI import Target


def client() -> Target:
    load_dotenv()
    key = os.getenv("KEY")
    if not key:
        raise ValueError("T_URL is not set")
    return Target(api_key=key)