import os
import pymysql.err
import pymysql.cursors
from dotenv import load_dotenv
import src.constants as constants

load_dotenv()

HOST = os.environ.get("MYSQL_HOST")
USER = os.environ.get("MYSQL_USER")
PASSWORD = os.environ.get("MYSQL_PASSWORD")
DB = os.environ.get("DB")
PORT = int(os.environ.get("MYSQL_PORT"))


def connection():
    try:
        return pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            db=DB,
            port=PORT,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except pymysql.err.OperationalError as e:
        if e.args[0] == 1049:
            print("Database not found")
            conn = pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                port=PORT,
                cursorclass=pymysql.cursors.DictCursor,
            )
            with conn.cursor() as cursor:
                cursor.execute(f"CREATE DATABASE {DB}")
            return pymysql.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                db=DB,
                port=PORT,
                cursorclass=pymysql.cursors.DictCursor,
            )
        else:
            print(e)
            exit()


def query(conn, sql, values=[]):
    with conn.cursor() as cursor:
        cursor.execute(sql, values)
        result = cursor.fetchall()
        return result


def auto_commit(conn, sql, values=[]):
    with conn.cursor() as cursor:
        cursor.execute(sql, values)
        conn.commit()

def get_highest_id(conn, table_name):
    sql_query = f"SELECT * FROM {table_name} ORDER BY {table_name}_id DESC"
    with conn.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchone()
        return result

def select_all_from_table(conn, table_name):
    sql_query = f"SELECT * FROM {table_name}"
    try:
        return query(conn, sql_query)
    except pymysql.err.ProgrammingError as e:
        if e.args[0] == 1146:
            print("Table not found")
            sql_query = f"CREATE TABLE {table_name}"
            table_query = ""
            for key in constants.get_keys(table_name):
                if key.split("_")[-1] == "id":
                    if key.split("_")[0] == table_name:
                        table_query += f"{key} {constants.VARIABLE_DB_TYPES[key.split('_')[-1]]} NOT NULL AUTO_INCREMENT PRIMARY KEY,"
                    else:
                        table_query += f"{key} {constants.VARIABLE_DB_TYPES[key.split('_')[-1]]} NOT NULL,CONSTRAINT fk_{key.split('_')[0]} FOREIGN KEY ({key}) REFERENCES {key.split('_')[0]}({key}),"
                else:
                    table_query += (
                        f"{key} {constants.VARIABLE_DB_TYPES[key.split('_')[-1]]},"
                    )
            table_query = table_query[:-1]  # remove last trailing comma
            sql_query += f"({table_query})"
            print(sql_query)
            query(conn, sql_query)
            return []
        else:
            print(e)
            exit()

#Add row to table in DB
def insert_into_table(conn, table_name, values):
    table_keys = list(values.keys())
    vars_amount = ""
    for each in table_keys:
        vars_amount += "%s,"
    vars_amount = vars_amount[:-1]
    auto_commit(conn, f"INSERT INTO {table_name}({','.join(table_keys)}) VALUES ({vars_amount})", tuple(values[key] for key in table_keys))