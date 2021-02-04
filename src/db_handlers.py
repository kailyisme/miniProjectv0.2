import os
import pymysql.cursors
from dotenv import load_dotenv

load_dotenv()

HOST = os.environ.get("HOST")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
DB = os.environ.get("DB")
PORT = int(os.environ.get("PORT"))

connection = pymysql.connect(host=HOST, user=USER, password=PASSWORD, db=DB, port=PORT)

print(connection)