from dotenv import dotenv_values
from database import PostgreSQL
import os

database = PostgreSQL()

def get_app_config(env_file_path: str) -> dict:
    def get_value(key: str, default: any = "") -> str:
        return os.environ.get(key) or env_config.get(key) or default
    
    env_config = dotenv_values(env_file_path)

    config = {}
    config["RABBIT_HOST"] = get_value("RABBIT_HOST")
    config["RABBIT_QUEUE"] = get_value("RABBIT_QUEUE")
    config["RABBIT_USERNAME"] = get_value("RABBIT_USERNAME")
    config["RABBIT_PASSWORD"] = get_value("RABBIT_PASSWORD")

    return config