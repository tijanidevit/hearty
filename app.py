# from msilib.schema import Environment
from flask import Flask
from flaskext.mysql import MySQL
from config import Config
from users import users_bp
from predictions import predictions_bp
from diseases import diseases_bp
import sys
from flask_cors import CORS
app = Flask(__name__)


CORS(app)
app.config.from_object(Config)
mysql = MySQL()
mysql.init_app(app)

app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(predictions_bp, url_prefix='/predictions')
app.register_blueprint(diseases_bp, url_prefix='/diseases')


@app.route('/')
def hello():
    return "Hello from Home Page"

@app.route('/setup', methods=['GET'])
def createTables():
    try:
        createUsersTable()
        createPredictionHistoriesTable()
        createAdminTable()
        createDiseaseTable()
        createDoctorTable()
        return "a"
    except:
        return sys.exc_info()[0]


def createUsersTable():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE users")
        conn.commit()
        test = cursor.execute(
            "CREATE TABLE users("
            "id int NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "fullname varchar(190),"
            "email varchar(190),"
            "age varchar(190),"
            "gender varchar(190),"
            "password text,"
            "created_at timestamp DEFAULT CURRENT_TIMESTAMP"
            ")")
        conn.commit()
    except:
        print(sys.exc_info()[0])


def createPredictionHistoriesTable():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        test = cursor.execute(
            "CREATE TABLE prediction_histories("
            "id int NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "user_id int,"
            "disease varchar(190),"
            "status int,"
            "created_at timestamp DEFAULT CURRENT_TIMESTAMP"
            ")")
        conn.commit()
    except:
        print(sys.exc_info()[0])


def createDoctorTable():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        test = cursor.execute(
            "CREATE TABLE doctors("
            "id int NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "disease_id INT,"
            "fullname varchar(190),"
            "image varchar(190),"
            "phone varchar(190),"
            "email varchar(190),"
            "bio text,"
            "created_at timestamp DEFAULT CURRENT_TIMESTAMP"
            ")")
        conn.commit()
    except:
        print(sys.exc_info()[0])


def createDiseaseTable():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        test = cursor.execute(
            "CREATE TABLE diseases("
            "id int NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "disease varchar(190),"
            "about text,"
            "cure text,"
            "created_at timestamp DEFAULT CURRENT_TIMESTAMP"
            ")")
        conn.commit()
    except:
        print(sys.exc_info()[0])


def createAdminTable():
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        test = cursor.execute(
            "CREATE TABLE admin("
            "id int NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "username varchar(190),"
            "password text,"
            "created_at timestamp DEFAULT CURRENT_TIMESTAMP"
            ")")
        conn.commit()
    except:
        print(sys.exc_info()[0])


# app.run(debug=True, host = "https://hearti-api.herokuapp.com/")
# app.run()
