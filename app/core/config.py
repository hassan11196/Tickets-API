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

MONGODB_URL = os.getenv("MONGODB_URL")  # deploying without docker-compose
MONGO_INITDB_DATABASE = os.getenv("MONGO_INITDB_DATABASE")
if MONGO_INITDB_DATABASE:
    print('Inside docker')
    # This is for specfic you dont need to change this
    MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
    MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))
    MONGO_USER = os.getenv("MONGO_USER", "admin")
    MONGO_PASS = os.getenv("MONGO_PASSWORD", "password")
    MONGO_DB = os.getenv("MONGO_DB", "tickets-test")

    MONGODB_URL = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:{MONGO_PORT}/{MONGO_DB}"
    
else:
    # Put your Mongo DB URL here,
    # This is a url for a mongodb server I created
    MONGODB_URL = 'mongodb://heroku_kk8c9mdc:rkhdsjgdds5m6bi943acvcd2hr@ds053429.mlab.com:53429/heroku_kk8c9mdc?retryWrites=false&w=majority'
    MONGO_DB = 'heroku_kk8c9mdc'
print(MONGODB_URL)

database_name = MONGO_DB
ticket_collection_name = "ticketEvents"

# MONGO_HOST=db
# MONGO_PORT=27017
# MONGO_USER=admin
# MONGO_PASSWORD=password
# MONGO_DB=tickets-test
# PORT=80