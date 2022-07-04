import sys
from flask import Blueprint, Flask, jsonify
from flaskext.mysql import MySQL
from config import Config
from flask import request
from flask_cors import CORS

users_bp = Blueprint('users', __name__)
app = Flask(__name__)
CORS(app)
app.config.from_object(Config)
mysql = MySQL()


mysql.init_app(app)

@users_bp.route('/register', methods=['POST'])
def registerAction():
    
    user_data = request.get_json()

    if not user_data['name'] or not user_data['email'] or not user_data['password']:
        return (jsonify({
            'success': 'false',
            'message': request.get_json(),
            'status': 200
        }))
    else:
        fullname = user_data['name']
        email = user_data['email']
        password = user_data['password']

        if checkEmail(email) > 0:
            return (jsonify({
                'success': 'false',
                'message': 'Email already exist',
                'status': 200
            }))

        conn = mysql.connect()
        cursor = conn.cursor()
        test = cursor.execute(
            "INSERT INTO users(fullname,email,password) VALUES('" + fullname + "','" + email + "','" + password + "')")

        if test:
            conn.commit()
            return (jsonify({
                'success': 'true',
                'message': 'Registration Successful',
                'data': getUser(email),
                'status': 201
            }))


@users_bp.route('/login', methods=['POST'])
def loginAction():
    user_data = request.get_json()

    if not user_data['email'] or not user_data['password']:
        return (jsonify({
            'success': 'false',
            'message': 'Please enter all the fields',
            'status': 200
        }))
    else:
        email = user_data['email']
        password = user_data['password']

        if checkEmail(email) < 1:
            return (jsonify({
                'success': 'false',
                'message': 'Email not found',
                'status': 200
            }))

        if login(email, password):

            return (jsonify({
                'success': 'true',
                'message': 'Login Successful',
                'data': getUser(email),
                'status': 200
            }))
        else:
            return (jsonify({
                'success': 'false',
                'message': 'Invalid Credentials',
                'status': 200
            }))


@users_bp.route('/update', methods=['POST'])
def updateAction():
    user_data = request.get_json()

    if not user_data['email']:
        return (jsonify({
            'success': 'false',
            'message': 'Please enter the email address',
            'status': 200
        }))

    if not user_data['age']:
        return (jsonify({
            'success': 'false',
            'message': 'Please enter age',
            'status': 200
        }))

    if not user_data['gender']:
        return (jsonify({
            'success': 'false',
            'message': 'Please select gender',
            'status': 200
        }))
    else:
        email = user_data['email']
        age = user_data['age']
        gender = user_data['gender']

        user = getUser(email)
        if not user:
            return (jsonify({
                'success': 'false',
                'message': 'Email not found',
                'status': 200
            }))
            
        else:
            user_id = (user['id'])
            if updateProfile(age, gender, user_id):
                return (jsonify({
                    'success': 'true',
                    'message': 'Profile Updated Successfully',
                    'data': getUser(email),
                    'status': 200
                }))
            else:
                print(sys.exc_info())
                return (jsonify({
                    'success': 'false',
                    'message': 'Unable to update',
                    'status': 200
                }))



def checkEmail(email):
    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("SELECT id FROM users WHERE email = '" + email + "'")
    return test


def getUser(email):
    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("SELECT * FROM users WHERE email = '" + email + "'")
    if test:
        user = cursor.fetchone()
        result = {
            'id': user[0],
            'fullname': user[1],
            'email': user[2],
            'gender': user[4],
            'age': user[3],
            'created_at': user[6],
        }

        return result
    return 'false'


def login(email, password):
    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("SELECT id FROM users WHERE email = '" + email + "' AND password =  '" + password + "'")
    return test


def updateProfile(age, gender, id):
    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("UPDATE users SET age = '" + age + "', gender =  '" + gender + "' WHERE id = '" + str(id) + "'")
    if test:
        conn.commit()
    return test
