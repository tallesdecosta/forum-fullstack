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
            user_id serial PRIMARY KEY,
            username text,
            password Varchar(255),
            email Varchar(255),
            avatar_path Varchar(255)
                );
                   """)
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

def create_table_posts():

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS posts (
            user_id serial references users(user_id),
            post_id serial PRIMARY KEY,
            title text,
            content text,
            likes INTEGER,
            comments INTEGER,
            was_made timestamp,
            image_path Varchar(255)
                );
                   """)
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

def create_table_comments():

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS comments (
            user_id serial references users(user_id),
            post_id serial references posts(post_id),
            content text,
            was_made timestamp,
            likes integer
                );
                   """)
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()

def insert_user(username, hash_password, email):
    """Insert new user row (user_id, username, password hash, email, image_path) in the table users."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO users (username, password, email, image_path) VALUES (%s, %s, %s, %s);""", 
    (username, hash_password, email, 'no-pic.jpg'))
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

def select_username_with_username(user):
    """Selects the user's username from the database using their user as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT username FROM users WHERE username = %s;""", (user,))
        username = cur.fetchone()

    except Exception as err:
        print(err)
        return err

    con.close()
    cur.close()
    if (username is not None):
        return username[0]
    else:
        return 'none'

def select_email_with_email(email):
    """Selects the user's email from the database using the provided email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT email FROM users WHERE email = %s;""", (email,))
        email_db = cur.fetchone()

    except Exception as err:
        print(err)
        return err

    con.close()
    cur.close()

    if(email_db is not None):
        return email_db[0]
    else:
        return 'none'

def select_data(email):
    """Selects the user's id, username, email and password hash from the database using their email as the parameter."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute(
        """SELECT user_id, username, email, password, avatar_path FROM users WHERE email=(%s);""", (email,))
        data = cur.fetchone()
        con.close()
        cur.close()

        if (data is not None):
            return data[0], data[1], data[2], data[3], data[4]
        else:
            return 'none'
        
    except Exception as err:
        print(err)


def update_username(id, username):
    """Updates the user's username in the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""UPDATE users SET username = %s WHERE user_id = %s;""", (username, id))
        con.commit()
        con.close()
        cur.close()

    except Exception as err:
        print(err)

    

def get_posts():
    """Gets posts from the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""SELECT user_id, post_id, title, content, likes, comments, was_made::varchar, image_path FROM posts LIMIT 5""")
        posts = cur.fetchall()
        con.close()
        cur.close()
        
        if posts:
            return [{'user_id': post[0], 'post_id': post[1], 'title': post[2], 'content': post[3], 'likes': post[4], 'comments': post[5],'was_made': post[6], 'image_path': post[7]} for post in posts]
        
        else:
            return 'none'
        
    except Exception as err:
        print(err)

def update_password(id, password):
    """Updates the user's password hash inside the database."""

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""UPDATE users SET password = %s WHERE user_id = %s;""", (password, id))
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()


def delete_user(id):

    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""DELETE FROM posts WHERE user_id=%s;""", (id,))
        cur.execute("""DELETE FROM users WHERE user_id=%s;""", (id,))
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()


def insert_posts(data):
    print(data)
    con = connect_database()
    cur = con.cursor()

    try:
        cur.execute("""INSERT INTO posts(user_id, title, content, likes, comments, was_made, image_path) VALUES(%s, %s, %s, %s, %s, to_timestamp(%s, 'DD-MM-YYYY HH24:MI:SS'), %s)""", (data['user'], data['title'], data['content'], 0, 0, data['datetime'], 'no-pic.jpg',))
        con.commit()
    except Exception as err:
        print(err)

    con.close()
    cur.close()