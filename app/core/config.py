import os

from dotenv import load_dotenv
from starlette.datastructures import CommaSeparatedStrings, Secret
# from databases import DatabaseURL



load_dotenv(".env")

MAX_CONNECTIONS_COUNT = int(os.getenv("MAX_CONNECTIONS_COUNT", 10))
MIN_CONNECTIONS_COUNT = int(os.getenv("MIN_CONNECTIONS_COUNT", 10))
SECRET_KEY = Secret(os.getenv("SECRET_KEY", "secret key for project"))

PROJECT_NAME = os.getenv("PROJECT_NAME", "FastAPI example application")
ALLOWED_HOSTS = CommaSeparatedStrings(os.getenv("ALLOWED_HOSTS", ""))

MONGODB_URL = os.getenv("MONGODB_URL", "")  # deploying without docker-compose
if not MONGODB_URL:
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "password")
    MONGO_DB = os.getenv("MONGO_DB", "tickets-test")

    MONGODB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    
else:
    MONGODB_URL = DatabaseURL(MONGODB_URL)


# MONGO_USER = "testuser"
# MONGO_PASS = "testpassword"
# MONGO_DB = 'test11196'
# MONGO_HOST = 'test11196-sayz6.mongodb.net'

# MONGODB_URL = "mongodb+srv://testuser:testpassword@test11196-sayz6.mongodb.net/test?retryWrites=true&w=majority";


database_name = MONGO_DB
ticket_collection_name = "tickets"
