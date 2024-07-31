from dotenv import load_dotenv
import os

def get_config():
    load_dotenv(verbose=True, override=True)
    username = os.getenv("ACCOUNT_USERNAME")
    password = os.getenv("ACCOUNT_PASSWORD")
    return username, password