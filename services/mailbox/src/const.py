import os

DB_HOST = os.getenv("DB_HOST")

SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://postgres:postgres@{DB_HOST}/postgres"
SECRET_KEY = open('/var/data/secret_key', 'rb').read()
