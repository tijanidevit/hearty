import json

from flask import Blueprint, Flask, jsonify
from flaskext.mysql import MySQL
from config import Config
from flask import request
import pickle



predictions_bp = Blueprint('predictions', __name__)
app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL()

mysql.init_app(app)



@predictions_bp.route('/', methods=['GET'])
def predictTest():
    filename = 'heart_model.pkl'
    model_reloaded = pickle.load(open(filename, 'rb'))

    res = model_reloaded.predict([[67,1,4,160,286,0,2,108,1,1.5,2,3,3]])[0]
    disease =''
    if res == 0:
        disease = "None"
    elif res == 1:
        disease = "Endocarditis"
    elif res == 2:
        disease = "Arrhythmias"
    elif res == 3:
        disease = "Cardiomyopathy (Heart Muscle Disease)"
    elif res == 4:
        disease = "Pericarditis"

    print(res)
    res = str(res)
    return (jsonify({
            'success': 'true',
            'message': 'Diagnosis Completed',
            'data' : disease,
            'status': 200
        }))



@predictions_bp.route('/<user_id>', methods=['POST'])
def prediction(user_id):
    form_data = request.form
    data = [form_data['age'], form_data['sex'], form_data['cp'], form_data['trestbps'], form_data['chol'],
              form_data['fbs'], form_data['restecg'], form_data['thalach'], form_data['exang'], 
              form_data['oldpeak'], form_data['slope'], form_data['ca'], form_data['thal']]
    
    if not user_id or user_id == '':
        return (jsonify({
            'success': 'false',
            'message': 'User ID is required',
            'status': 200
        }))
    if checkUser(user_id) < 1:
        return (jsonify({
            'success': 'false',
            'message': 'User not found',
            'status': 200
        }))

    filename = 'heart_model.pkl'
    model_reloaded = pickle.load(open(filename, 'rb'))

    res = model_reloaded.predict([data])[0]
    disease =''
    status = 1
    if res == 0:
        disease = "None"
        status = 0
    elif res == 1:
        disease = "Endocarditis"
    elif res == 2:
        disease = "Arrhythmias"
    elif res == 3:
        disease = "Cardiomyopathy (Heart Muscle Disease)"
    elif res == 4:
        disease = "Pericarditis"

    savePredictHistory(user_id, disease, status)
    return (jsonify({
            'success': 'true',
            'message': 'Diagnosis Completed',
            'data' : disease,
            'status': 200
        }))
        


@predictions_bp.route('/<user_id>', methods=['GET'])
def fullHistory(user_id):
    if not user_id or user_id == '':
        return (jsonify({
            'success': 'false',
            'message': 'User ID is required',
            'status': 200
        }))
    if checkUser(user_id) < 1:
        return (jsonify({
            'success': 'false',
            'message': 'User not found',
            'status': 200
        }))

    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("SELECT * FROM prediction_histories WHERE user_id = " + user_id + "LIMIT 7")

    if test:
        data = cursor.fetchall()

        result = []
        for hist in data:
            result.append({
                'id': hist[0],
                'user_id': hist[1],
                'keyword': hist[2],
                'status': hist[3],
                'created_at': hist[4],
            })
        return jsonify({
            'success': 'true',
            'message': 'Previous Predictions Fetch Successfully',
            'data': result,
            'status': 200
        })
    return 'false'


@predictions_bp.route('history/<user_id>', methods=['GET'])
def history(user_id):
    if not user_id or user_id == '':
        return (jsonify({
            'success': 'false',
            'message': 'User ID is required',
            'status': 200
        }))
    if checkUser(user_id) < 1:
        return (jsonify({
            'success': 'false',
            'message': 'User not found',
            'status': 200
        }))

    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("SELECT * FROM prediction_histories WHERE user_id = " + user_id + "LIMIT 7")

    if test:
        data = cursor.fetchall()

        result = []
        for hist in data:
            result.append({
                'id': hist[0],
                'user_id': hist[1],
                'keyword': hist[2],
                'status': hist[3],
                'created_at': hist[4],
            })
        return jsonify({
            'success': 'true',
            'message': 'Previous Predictions Fetch Successfully',
            'data': result,
            'status': 200
        })
    return 'false'


def savePredictHistory(user_id, disease, status):

    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("INSERT INTO prediction_histories(user_id,disease,status) VALUES(" + user_id + ",'" + disease + "','" + str(status) + "')")

    if test:
        conn.commit()
        return 'true'
    return 'false'


def checkUser(user_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    test = cursor.execute("SELECT id FROM users WHERE id = '" + user_id + "'")
    return test
