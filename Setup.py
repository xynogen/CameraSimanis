import sqlalchemy as db
import os
from dotenv import load_dotenv


load_dotenv()

TEMP_FOLDER = os.environ['TEMP_FOLDER']
API_KEY = os.environ['API_KEY']
DB_NAME = os.environ['DB_NAME']
DB_URI = f'sqlite:///{DB_NAME}'


# check if temp folder exist
if not os.path.exists(TEMP_FOLDER):
    os.mkdir(TEMP_FOLDER)

# delete old database
if os.path.exists(DB_NAME):
    os.remove(DB_NAME)

# create the engine handler
engine = db.create_engine(DB_URI)
# create database table for saving the API Key
engine.execute("""
    CREATE TABLE 'api_keys' (
        id INTEGER NOT NULL,
        api_key VARCHAR(36),
        PRIMARY KEY (id)
    );
""")

engine.execute(f"""
    INSERT INTO 'api_keys'
    (api_key)
    VALUES ('{API_KEY}')
""")

