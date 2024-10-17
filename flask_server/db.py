from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

sqlite_uris = {
    "development": "sqlite:///dev.db",
    "production": "sqlite:///prod.db",
    "test": "sqlite:///test.db"
}
load_dotenv()

def get_database_uri():
    env = os.getenv('environment')
    if env not in sqlite_uris.keys():
        raise ValueError("Invalid environment")
    
    return sqlite_uris[env]