from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

def connect_database():

    try:
        connection = psycopg2.connect(host=os.getenv("host"), 
                                      dbname=os.getenv("dbname"), 
                                      user=os.getenv("user"), 
                                      password=os.getenv("password"),
                                      port=os.getenv("port"))

    except Exception as err:
        print(err)

    return connection

def create_table_users():
    """Create the table users if it does not already exists."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
            id serial PRIMARY KEY,
            username text,
            password Varchar(255),
            email Varchar(255),
            image_path Varchar(255)
                );
                   """)
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

def insert_user(username, hash_password, email):
    """Insert new user row (id, username, password hash, email) in the table users."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO users (username, password, email) VALUES (%s, %s, %s);""", 
    (username, hash_password, email))
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

def select_password(email):
    """Selects the user's password from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT password FROM users WHERE email = (%s);""", (email,))
        password = cur.fetchone()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

    return password[0]

def select_username(email):
    """Selects the user's username from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT username FROM users WHERE email = %s;""", (email,))
        username = cur.fetchone()

    except Exception as err:
        print(err)

    con.close()
    cur.close()

    return username[0]

def select_data(email):
    """Selects the user's id, username, email and password hash from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute(
        """SELECT id, username, email, password FROM users WHERE email=(%s);""", (email,))
        data = cur.fetchone()
    except Exception as err:
        print(err)


    con.close()
    cur.close()

    return data[0], data[1], data[2], data[3]

def update_username(id, username):
    """Updates the user's username in the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""UPDATE users SET username = %s WHERE id = %s;""", (username, id))
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

def update_password(id, password):
    """Updates the user's password hash inside the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""UPDATE users SET password = %s WHERE id = %s;""", (password, id))
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()