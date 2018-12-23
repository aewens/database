from os import urandom
from os.path import exists
from sqlite3 import connect
from hashlib import sha256
from binascii import hexlify

def binhash():
    m = sha256()
    m.update(urandom(32))
    return m.digest()

def hexhash(binary):
    return hexlify(binary).decode()

def open_database(database_name):
    conn = connect(database_name)
    cursor = conn.cursor()
    return {
        "conn": conn, 
        "cursor": cursor
    }

def close_database(db):
    conn = db.get("conn", None)
    if conn is not None:
        conn.close()

def create_tables(db):
    conn = db.get("conn", None)
    c = db.get("cursor", None)
    if not (conn or c):
        return False
    users_table = """
    CREATE TABLE users (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        hash BINARY(32), 
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    c.execute(users_table)
    conn.commit()
    return True

def sanitize(data):
    return "".join(char for char in data if char.isalnum())

def add_record(db, table, record):
    conn = db.get("conn", None)
    c = db.get("cursor", None)
    if not (conn or c):
        return False
    clean_table = sanitize(table)
    keys = list(record.keys())
    clean_keys = ", ".join(list(map(sanitize, keys)))
    values = ", ".join(list(record.values()))
    statement = "INSERT INTO {} ({}) VALUES (?)".format(clean_table, clean_keys)
    c.execute(statement, (values,))
    conn.commit()
    return True

def get_records(db, table):
    conn = db.get("conn", None)
    c = db.get("cursor", None)
    if not (conn or c):
        return False
    clean_table = sanitize(table)
    c.execute("SELECT * FROM {}".format(clean_table))
    records = c.fetchall()
    return records