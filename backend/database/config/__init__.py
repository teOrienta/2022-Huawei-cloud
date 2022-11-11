from .db_config import verify_connection
from .db_connection import DBConnectionHandler
from .db_base import Base, classproperty
from dotenv import dotenv_values
import os

def get_value(key: str, default: any = "") -> any:
    return os.environ.get(key) or env_config.get(key, default)
    
CONFIG_PATH = ".env"
env_config = dotenv_values(CONFIG_PATH)
port = get_value("DB_PORT", "5432")
host = get_value("DB_HOST", "localhost")
user = get_value("DB_USER", "")
password = get_value("DB_PASSWORD", "")
database = get_value("DB_DATABASE", "")
connection_pool_size = int(get_value("CONNECTION_POOL_SIZE", "50"))

conn_string = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
db_conn = DBConnectionHandler(conn_string, connection_pool_size)