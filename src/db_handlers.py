import os
from dotenv.main import get_key
import pymysql.err
import pymysql.cursors
from dotenv import load_dotenv
import src.constants as constants
import uuid

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
                elif key.split("_")[-1] == "uuid":
                    if key.split("_")[0] == table_name:
                        table_query += f"{key} {constants.VARIABLE_DB_TYPES[key.split('_')[-1]]} NOT NULL PRIMARY KEY,"
                    else:
                        table_query += f"{key} {constants.VARIABLE_DB_TYPES[key.split('_')[-1]]} NOT NULL,CONSTRAINT fk_{key.split('_')[0]} FOREIGN KEY ({key}) REFERENCES {key.split('_')[0]}({key}) ON DELETE CASCADE,"
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


# Add row to table in DB
def insert_into_table(conn, table_name, values: dict):
    table_keys = list(values.keys())
    vars_amount = ""
    for each in table_keys:
        vars_amount += "%s,"
    vars_amount = vars_amount[:-1]
    auto_commit(
        conn,
        f"INSERT INTO {table_name}({','.join(table_keys)}) VALUES ({vars_amount})",
        tuple(values[key] for key in table_keys),
    )


# Add row to table in DB
def replace_into_table(conn, table_name, values: dict):
    table_keys = list(values.keys())
    vars_amount = ""
    for each in table_keys:
        vars_amount += "%s,"
    vars_amount = vars_amount[:-1]
    print(f"REPLACE INTO {table_name}({','.join(table_keys)}) VALUES ({vars_amount})",
        tuple(values[key] for key in table_keys))
    auto_commit(
        conn,
        f"REPLACE INTO {table_name}({','.join(table_keys)}) VALUES ({vars_amount})",
        tuple(values[key] for key in table_keys),
    )


def get_highest_id(conn, table_name):
    return query(
        conn, f"SELECT * FROM {table_name} ORDER BY {table_name}_id DESC LIMIT 1"
    )[0]


# Update row in table in DB
def update_row_on_table(conn, table_name, values, id, is_uuid=False):
    keys_to_update = list(values.keys())
    values_to_update = tuple(values[each] for each in keys_to_update)
    set_string = ""
    for key in keys_to_update:
        set_string += f"{key}=%s,"
    set_string = set_string[:-1]
    id_append = "_id"
    if is_uuid == True:
        id_append = "_uuid"
        id = uuid.UUID(bytes=id).hex
        id = f"unhex('{id}')"
    auto_commit(
        conn,
        f"UPDATE {table_name} SET {set_string} WHERE {table_name}{id_append} = {id}",
        values_to_update,
    )


# Retrieve entry/row for {table_name}_id
def retrieve_row_for_id(conn, table_name, id, is_uuid=False):
    id_append = "_id"
    if is_uuid == True:
        id_append = "_uuid"
        # id = uuid.UUID(bytes=id).hex
        # id = f"unhex('{id}')"
    return query(conn, f"SELECT * FROM {table_name} WHERE {table_name}{id_append} = %s", id)[0]


def delete_row_for_id(conn, table_name, id, is_uuid=False):
    id_append = "_id"
    if is_uuid == True:
        id_append = "_uuid"
        # id = uuid.UUID(bytes=id).hex
        # id = f"unhex('{id}')"
    auto_commit(conn, f"DELETE FROM {table_name} WHERE {table_name}{id_append}= %s", id)


def new_order(conn, customer_id, courier_id):
    a_uuid = uuid.uuid4().hex  # uuid.UUID(hex=a_uuid) to pack again from hex to uuid
    transaction_status = constants.TRANSACTION_STATUSES[0]
    auto_commit(
        conn,
        f"INSERT INTO transaction VALUES (unhex(%s),now(),%s,%s,%s) ",
        (a_uuid, customer_id, courier_id, transaction_status),
    )


def get_most_recent_order(conn):
    keys = constants.get_keys("transaction")
    return query(
        conn,
        f"SELECT {','.join(key for key in keys)} FROM transaction ORDER BY transaction_time DESC",
    )[0]
