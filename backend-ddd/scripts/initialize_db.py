"""
To load the environment variables using the dotenv from the .env file
"""
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    host=os.environ.get("DB_HOST"),
    database=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASSWORD"),
    port=os.environ.get("DB_PORT"),
)
cursor = connection.cursor()

with open("../my_spots/db/initialize-db.sql") as sql_init:
    sql = sql_init.read()

    cursor.execute(sql)
    connection.commit()

    print("MySpots db successfully resetted and initialized!")
