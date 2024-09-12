import psycopg2
import auth as auth
import database as database
from flask import Flask, request, render_template, redirect, session, url_for
from dotenv import load_dotenv
import bcrypt
import os
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

load_dotenv()

## flask constructor

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = os.getenv("key")
    database.create_table_users()
    return app

app = create_app()

log = LoginManager()
log.init_app(app)

class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

    @staticmethod
    def get(userId):
        con = database.connect_database()
        cur = con.cursor()

        try:
            cur.execute("SELECT id, username, email FROM users WHERE id = (%s)", (userId))
            data = cur.fetchone()
        except Exception as err:
            print(err)

        con.close()
        cur.close()

        if data:
            return User(data[0], data[1], data[2])
        
        return None

@log.user_loader
def load_user(userId):
    return User.get(userId)

## routing
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/feed')
@login_required
def feed():
    return render_template("feed.html")


@app.route('/login')
def login():
    auth = request.args.get("auth", "true")
    if current_user.is_authenticated:
        return redirect("/", 301)
    else:
        return render_template('login.html', auth = auth)

@app.route('/login', methods =["GET","POST"])
def login_post():
    if request.method == "POST":

        form_email = request.form.get("email")
        form_password = request.form.get("password")

        id, username, email, password = database.select_data(form_email)

        if auth.compare_password(form_password, password) == True:
            user = User(id, username, email)
            login_user(user)
            return redirect("/", 301)
        
        else:
            return "You are not logged in"
        
@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/account')
@login_required
def account():
    return render_template("account.html")

@app.route('/account', methods = ["GET", "POST"])
def change_information():
    if request.form.get("type") == "username":
        username = request.form.get("username")

        database.update_username(current_user.id, username)

        return redirect("/account", 301)
    
    elif request.form.get("type") == "password":
        password = request.form.get("password")

        if auth.validate_password(password) == True:
            hash_password = auth.encrypt_password(password)

            try: 
                database.update_password(current_user.id, hash_password)
            except Exception as err:
                print(err)
            
            return redirect("/account", 301)
        
        else:
            return redirect("/account", 402)
        

@app.route('/logout')
def logout():
    logout_user()
    return redirect("/", 302)

@app.route('/register', methods =["GET", "POST"])
def register_post():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        username = request.form.get("username")

        email_valid, password_valid, username_valid = auth.validate_register(email, password, username)

        if email_valid == True and password_valid == True and username_valid == True:
            hashed_password = auth.encrypt_password(password)
            database.create_table_users()
            database.insert_user(username, hashed_password, email)
            return redirect("/", 302)
        
        else:
            return "Registration failed"

@log.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for("login", auth = "false"))

if __name__ == '__main__':
    app.run()
