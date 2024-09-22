# About The Project

This project consists of a fullstack forum web application. 

- Dynamic posts and profiles URL
- Password encryptation
- Full CRUD interactions for the user's data

[Video presentation of the project will be made as soon as it is done.]

## Built With

![flask](https://img.shields.io/badge/Flask-563D7C?style=for-the-badge&logo=flask&logoColor=white)

![postgresql](https://img.shields.io/badge/Postgresql-4ca63a?style=for-the-badge&logo=postgresql&logoColor=white)

# Getting Started

After you initiated a venv inside the project folder, run the following command inside the terminal:

```
pip install flask flask-login psycopg2 python-dotenv bcrypt
```

After all the requisites are installed, just create a ```.env``` file and fill with your database information:

```
host=""
dbname=""
user=""
password=""
port=""
key=""
```

PS: the 'key' field is reserved for the Flask application key, you should fill it with a (secure) value for the application to work.

Then run the following command inside the src folder:

```
flask --app server run
```


And it's done! The server should create the databases and tables automatically.