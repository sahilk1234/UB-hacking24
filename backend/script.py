import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
print("Connected to the database successfully")
conn.close()
